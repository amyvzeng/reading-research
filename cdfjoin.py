#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cdfsampler
import natjoin
import loadimdb
import minhash
import random
import time
import copy


# In[2]:


def normalize(lower, upper, value):
    return (float(value) - float(lower)) / (float(upper) - float(lower))


# In[3]:


def remove_hashsum_key(tables):
    for table in tables:
        for entry in table:
            if "hash sum" in entry.keys():
                del entry["hash sum"]
                
    return tables


# In[4]:


def cdfjoin(tables, sampling_threshold, timer=0):
    if len(tables) <= 1:
        return tables
    else:
        attrs = {}
        join_attrs = []
        
        #find join attributes
        for i in range(len(tables)):
            table = tables[i]
            for table_key in table[0].keys():
                if table_key in attrs.keys(): attrs[table_key].append(i)
                else: attrs[table_key] = [i]
        join_attrs = [k for k,v in attrs.items() if len(v) > 1]
        
        #generate hash functions for each join_attr
        hash_functions = minhash._generate_hash_fns(len(join_attrs))
        attrs_hash_dict = {join_attrs[i]: hash_functions[i] for i in range(len(hash_functions))}
        
        #copy tables
        tables_copy = []
        for table in tables:
            tables_copy.append(copy.deepcopy(table))
        
        #calculate hash sum for each entry in each table
        for table in tables_copy:
            table_attrs = [key for key in table[0].keys() if key in join_attrs]
            norm_hashed_table = {}
            hashed_table = {}
            hashed_table = {attr: minhash._min_hash([attr], table, attrs_hash_dict[attr]) for attr in table_attrs}
            for k,v in hashed_table.items():
                norm_v = {normalize(0, minhash.NEXTPRIME, v1): v2 for v1, v2 in v.items()}
                norm_hashed_table[k] = norm_v
            for i in range(len(table)):
                entry = table[i]
                hash_scores = []
                for k, v in norm_hashed_table.items():
                    for v1, v2 in v.items():
                        if i in v2:
                            hash_scores.append(v1)
                            break
                entry["hash sum"] = sum(hash_scores)
        
        #filter for all entries whose cdf <= sampling probability
        filtered_tables = []
        start = time.time()
        for i in range(len(tables)):
            table = tables_copy[i]
            filtered_table = []
            if "hash sum" in table[0].keys():
                n_join_attrs = len([i for i in table[0].keys() if i in join_attrs])
                for entry in table:
                    if cdfsampler.cdf(n_join_attrs, entry["hash sum"]) <= sampling_threshold:
                        filtered_table.append(entry)
            else:
                filtered_table = table
            if len(filtered_table) > 0:
                filtered_tables.append(filtered_table)
            else:
                filtered_tables = []
                break
        filtered_time = time.time() - start        

                
        #filter for all entries whose cdf <= random probability
        random_tables = []
        start = time.time()
        for i in range(len(tables)):
            table = tables_copy[i]
            random_threshold = random.uniform(0,1)
            random_table = []
            if "hash sum" in table[0].keys():
                n_join_attrs = len([i for i in table[0].keys() if i in join_attrs])
                for entry in table:
                    if cdfsampler.cdf(n_join_attrs, entry["hash sum"]) <= random_threshold:
                        random_table.append(entry)
            else:
                random_table = table
            if len(random_table) > 0:
                random_tables.append(random_table)
            else:
                random_tables = []
                break
        random_time = time.time() - start
        
        if filtered_tables == []:
            joined_filtered_tables = []
        else:
            filtered_tables = remove_hashsum_key(filtered_tables)
            start = time.time()
            joined_filtered_tables = natjoin.natural_join(filtered_tables)
            filtered_time += time.time() - start
            
        if random_tables == []:
            joined_random_tables = []
        else:
            random_tables = remove_hashsum_key(random_tables)
            start = time.time()
            joined_random_tables = natjoin.natural_join(random_tables)
            random_time += time.time() - start
            

        return [(joined_filtered_tables, filtered_time), (joined_random_tables, random_time)]


# In[5]:


cdfjoin(loadimdb.tables, .5)


# In[6]:


cdfjoin(loadimdb.tables, .3)


# In[ ]:




