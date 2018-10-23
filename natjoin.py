#!/usr/bin/env python
# coding: utf-8

# In[1]:


# example_table_one = [{"name": " ", "age": 21, "year": 1957},
#                     {"name": " ", "age": 21, "year": 1957},
#                     {"name": " ", "age": 21, "year": 1957},
#                     {"name": " ", "age": 21, "year": 1957},
#                     {"name": " ", "age": 21, "year": 1957},
#                     {"name": " ", "age": 21, "year": 1957}]
# example_table_two = [{"name": " ", "age": 21, "year": 1957, "g": "a"},
#                     {"name": " ", "age": 21, "year": 1957, "g": "b"},
#                     {"name": " ", "age": 21, "year": 1958, "g": "c"},
#                     {"name": " ", "age": 42, "year": 1958, "g": "d"},
#                     {"name": " ", "age": 42, "year": 1958, "g": "e"},
#                     {"name": " ", "age": 42, "year": 1958, "g": "f"}]
# example_table_three = [{"name": " ", "age": 21, "year": 1957, "h": "a"},
#                     {"name": " ", "age": 63, "year": 1959, "h": None},
#                     {"name": " ", "age": 63, "year": 1959, "h": None},
#                     {"name": " ", "age": 63, "year": 1959, "h": None},
#                     {"name": " ", "age": 21, "year": 1957, "h": None},
#                     {"name": " ", "age": 63, "year": 1959, "h": None}]
# example_table_four = [{"id": " ", "birth": " ", "death": " "}]


# In[2]:


def cartesian_product(r,s):
    output = []
    for r_entry in r:
        for s_entry in s:
            r_copy = r_entry.copy()
            r_copy.update(s_entry)
            output.append(r_copy)
    return output


# In[3]:


# cartesian_product(example_table_one, example_table_four)


# In[4]:


def classic_hash_join(r, s):
    r_attributes = r[0].keys()
    s_attributes = s[0].keys()
    common_attributes = list(filter(lambda ra: ra in s_attributes, r_attributes))
    if len(common_attributes) > 0:
        s_unique_attributes = list(filter(lambda sa: sa not in common_attributes, s_attributes))
        hashtable = {}
        hashtable_keys = []
        hashkey = ""
        
        #build hash table
        row_index = 0
        for entry in r:
            for attribute in common_attributes:
                hashkey += str(entry[attribute])
            if hashkey not in hashtable_keys:
                hashtable[hashkey] = [row_index]
                hashtable_keys.append(hashkey)
            else:
                hashtable[hashkey].append(row_index)
            hashkey = ""
            row_index+=1

        
        #join
        output = []
        for entry in s:
            for attribute in common_attributes:
                hashkey += str(entry[attribute])
            if hashkey in hashtable_keys:
                filtered_dict = {k:v for (k,v) in entry.items() if k in s_unique_attributes}
                for r_index in hashtable[hashkey]:
                    new_entry = (r[r_index].copy())
                    new_entry.update(filtered_dict)
                    output.append(new_entry)
            hashkey=""
        return output
    else:
        return cartesian_product(r,s)


# In[5]:


def natural_join(tables):
    l1 = tables[0]
    for i in range(1, len(tables)):
        l1 = classic_hash_join(l1, tables[i])
    return l1


# In[6]:


# natural_join([example_table_two, example_table_three])


# In[ ]:




