#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv


# In[2]:


aka_name = ["id", "person_id", "name", 
            "imdb_index", "name_pcode_cf", "name_pcode_nf", 
            "surname_code", "md5sum"]
aka_title = ["id", "movie_id", "title", 
             "imdb_index", "kind_id", "production_year", 
             "phonetic_code", "episode_of", "season_nr", 
             "episode_nr", "note", "md5sum"]
cast_info = ["id", "person_id", "movie_id",
            "person_role_id", "note", "nr_order",
            "role_id"]
char_name = ["id", "name", "imdb_index",
            "imdb_id", "name_pcode_nf", "surname_pcode",
            "md5sum"]
comp_cast_type = ["id", "kind"]
company_name = ["id", "name", "country_code",
               "imdb_id", "name_pcode_nf", "name_pcode_sf",
               "md5sum"]
company_type = ["id", "kind"]
complete_cast = ["id", "movie_id", "subject_id",
                "status_id"]
keyword = ["id", "keyword", "phonetic_code"]
kind_type = ["id", "kind"]
link_type = ["id", "link"]
movie_companies = ["id", "movie_id", "company_id",
                  "company_type_id", "note"]
movie_info_idx = ["id", "movie_id", "info_type_id",
                 "info", "note"]
movie_keyword = ["id", "movie_id", "keyword_id"]
movie_link = ["id", "movie_id", "linked_movie_id",
             "link_type_id"]
name = ["id", "name", "imdb_index",
       "imdb_id", "gender", "name_pcode_cf",
       "name_pcode_nf", "surname_pcode", "md5sum"]
role_type = ["id", "role"]
title = ["id", "title", "imdb_index",
        "kind_id", "production_year", "imdb_id",
        "phonetic_code", "episode_of_id", "season_nr",
        "series_years", "md5sum"]
movie_info = ["id", "movie_id", "info_type_id",
             "info", "note"]
# person_info = ["id", "person_id", "info_type_id",
#               "info", "note"]


# In[3]:


csv_names = {"aka_name": aka_name, "aka_title": aka_title, "cast_info": cast_info, "char_name": char_name,
            "comp_cast_type": comp_cast_type, "company_name": company_name, "company_type": company_type, 
             "complete_cast": complete_cast, "keyword": keyword, 
             "kind_type": kind_type, "link_type": link_type, "movie_companies": movie_companies, 
             "movie_info_idx": movie_info_idx, "movie_keyword": movie_keyword, "movie_link": movie_link,
            "name": name, "role_type": role_type, "title": title, "movie_info": movie_info}


# In[8]:


table_index_dict = {}
tables = []

for csv_title in ["aka_name", "aka_title", "cast_info"]:
    with open('./imdb/' + csv_title + '.csv', newline = '') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        table = []
        headers = csv_names[csv_title]
        counter = 0
        for row in spamreader:
            if counter > 100:
                break
            else:
                counter += 1
                table.append({headers[i]: row[i] for i in range(1,len(headers))})
        tables.append(table)


# In[9]:





# In[ ]:




