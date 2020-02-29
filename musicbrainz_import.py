import sqlite3
#中文繁简转换工具，Musicbrainz数据库中文均为繁体
from zhconv import convert

# Replace your own parameters
mbdump_path='mbdump/'
database_path='db.sqlite3'
prefix='musicbrainz_'

# Connect to the database
connection = sqlite3.connect(database_path)


'''
#Custom database table names .
# You may need to change table names if you integrate with your Django project.

old_prefix='sslog_musicbrainz_'
new_prefix='musicbrainz_'
tables=[
    'artist',
    'tag',
    'artist_tag',
    'release',
    'release_tag',
    'release_artist',
    'recording',
    'recording_tag',
    'recording_artist',
    'medium',
    'artist_credit_name'
]
for item in tables:
    sql = 'alter table ' + old_prefix + item + ' rename to ' + new_prefix + item
    try:
        connection.execute(sql)
    except sqlite3.OperationalError as e:
        print('no such table ' + old_prefix + item)  

connection.commit()
'''


# improt artist
with open(mbdump_path +'artist','rt',encoding='utf-8') as f:
    i = 0
    for line in f:
        data = line.split('\t')
        id= int(data[0])
        gid = str(data[1]).replace('-','')
        name = convert(str(data[2]), 'zh-hans')
        params = (id,gid,name)
        try:
            connection.execute("insert into " + prefix + "artist values(?,?,?)",params)
            if i % 10000 ==0:
            print('musicbrainz_artist\t' + str(i))
        except:
            if i % 10000 ==0:
                print('musicbrainz_artist\t' + str(i) + ' is exists')
        i += 1
connection.commit()

# improt artist_credit_name
with open(mbdump_path +'artist_credit_name','rt',encoding='utf-8') as f:
    i = 0
    for line in f:
        data = line.split('\t')
        artist_credit= int(data[0])
        artist = int(data[2])
        params = (None,artist_credit,artist)
        try:
            connection.execute("insert into " + prefix + "artist_credit_name values(?,?,?)",params)
            if i % 10000 ==0:
                print('musicbrainz_artist_credit_name\t' + str(i))
        except:
            if i % 10000 ==0:
                print('musicbrainz_artist_credit_name\t' + str(i) + ' is exists')
        i += 1
connection.commit()

# improt tag
with open(mbdump_path +'label','rt',encoding='utf-8') as f:
    i = 0
    for line in f:
        data = line.split('\t')
        id= int(data[0])
        gid = str(data[1]).replace('-','')
        name = convert(str(data[2]), 'zh-hans')
        params = (id,gid,name)
        try:
            connection.execute("insert into " + prefix + "tag values(?,?,?)",params)
            if i % 10000 ==0:
                print('musicbrainz_tag\t' + str(i))
        except:
            if i % 10000 ==0:
                print('musicbrainz_tag\t' + str(i) + ' is exists')

        i += 1
connection.commit()

# improt artist_label
with open(mbdump_path + 'l_artist_label','rt',encoding='utf-8') as f:
    i = 0
    for line in f:
        data = line.split('\t')
        artist_id = data[2]
        label_id= data[3]
        params = (None,artist_id,label_id)
        try:
            connection.execute("insert into " + prefix + "artist_tag values(?,?,?)" ,params)
            if i % 10000 ==0:
                print('musicbrainz_artist_label\t' + str(i))
        except:
            if i % 10000 ==0:
                print('musicbrainz_artist_label\t' + str(i) + ' is exists')

        i += 1
connection.commit()

# improt release
with open(mbdump_path + 'release','rt',encoding='utf-8') as f:
    i = 0
    for line in f:
        data = line.split('\t')
        id= int(data[0])
        gid = str(data[1]).replace('-','')
        name = convert(str(data[2]), 'zh-hans')
        artist_credit= str(data[3])
        params = (id,gid,name,artist_credit,0)
        try:
            connection.execute("insert into " + prefix + "release values(?,?,?,?,?)",params)
            
            if i % 10000 ==0:
                print('musicbrainz_release\t' + str(i))
        except:
            if i % 10000 ==0:
                print('musicbrainz_release\t' + str(i) + ' is exists')
        i += 1
connection.commit()

# Update the publishdate field in release by release_unknown_country
with open(mbdump_path + 'release_unknown_country','rt',encoding='utf-8') as f:
    i = 0
    for line in f:
        data = line.split('\t')
        id= data[0]
        publishdate = data[1]
        params = (name,id)
        try:
            connection.execute("update " + prefix + "release set publishdate=? where id=?" ,params)
            print('musicbrainz_release_publishdate\t' + str(i))
            if i % 10000 ==0:
                connection.commit()
        except:
            with open('error.txt','at',encoding='utf-8') as f:
                f.write('musicbrainz_release_unknown_country\t' + str(i) + '\t' +line)
                print('musicbrainz_release_unknown_country\t' + str(i) + ' is exists')

        i += 1
connection.commit()

# Update the publishdate field in release by release_country
with open(mbdump_path + 'release_country','rt',encoding='utf-8') as f:
    i = 1
    for line in f:
        data = line.split('\t')
        id= data[0]
        publishdate = data[2]
        params = (name,id)
        try:
            connection.execute("update " + prefix + "release set publishdate=? where id=?" ,params)
            print('musicbrainz_release_publishdate\t' + str(i))
            if i % 10000 ==0:
                connection.commit()
        except:
            with open('error.txt','at',encoding='utf-8') as f:
                f.write('musicbrainz_release_country\t' + str(i) + '\t' +line)
                print('musicbrainz_release_country\t' + str(i) + ' is exists')

        i += 1
connection.commit()


# improt release_artist
with open(mbdump_path + 'release','rt',encoding='utf-8') as f:
    i = 1
    for line in f:
        data = line.split('\t')
        id = data[0]
        artist_credit= str(data[3])
        cursor = connection.execute("select * from " + prefix + "artist_credit_name where artist_credit=" + artist_credit)
        for item in cursor:
            params = (None,id,item[2])
            try:
                connection.execute("insert into " + prefix + "release_artist values(?,?,?)" ,params)
                
                print('musicbrainz_release_artist\t' + str(i))
                if i % 10000 ==0:
                    connection.commit()
            except:
                with open('error.txt','at',encoding='utf-8') as f:
                    f.write('musicbrainz_release_artist\t' + str(i) + '\t' +line)
                    print('musicbrainz_release_artist\t' + str(i) +  ' is exists')
            i += 1

connection.commit()



# improt release_label
with open(mbdump_path + 'release_label','rt',encoding='utf-8') as f:
    i = 1
    for line in f:
        data = line.split('\t')
        
        try:
            release_id = int(data[1])
            label_id= int(data[2])
            params = (None,release_id,label_id)
            connection.execute("insert into " + prefix + "release_tag values(?,?,?)" ,params)
            print('musicbrainz_release_label\t' + str(i))
            if i % 10000 ==0:
                connection.commit()
        except:
            with open('error.txt','at',encoding='utf-8') as f:
                f.write('musicbrainz_release_label\t' +str(i) + '\t' +line)
                print('musicbrainz_release_label\t' +str(i) + ' is exists')
        i += 1

connection.commit()


# improt recording
with open(mbdump_path + 'recording','rt',encoding='utf-8') as f:
    i = 1
    for line in f:
        try:
            data = line.split('\t')
            id= int(data[0])
            gid = str(data[1]).replace('-','')
            name = convert(str(data[2]), 'zh-hans')
            params = (id,gid,name,1)
            connection.execute("insert into " + prefix + "recording values(?,?,?,?)" ,params)
            i += 1
            if i % 10000 == 0 :
                print('musicbrainz_recording\t' + str(i))
        except:
            print('musicbrainz_recording\t' + str(i) + ' is exists')
connection.commit()

# improt media
with open(mbdump_path + 'medium','rt',encoding='utf-8') as f:
    i = 1
    for line in f:
        data = line.split('\t')
        try:
            id= int(data[0])
            release=int(data[1])
            params = (id,release)
            connection.execute("insert into " + prefix + "media values(?,?)" ,params)
            print('musicbrainz_medium\t' + str(i))
        except:
            with open('error.txt','at',encoding='utf-8') as f:
                f.write('musicbrainz_medium\t' +str(i) + '\t' +line)
                print('musicbrainz_medium\t' +str(i) + '\t' +line)
        i += 1
connection.commit()


# improt recording_release
with open(mbdump_path + 'track','rt',encoding='utf-8') as f:
    i = 1
    for line in f:
        data = line.split('\t')
        
        try:
            recording_id = int(data[2])
            medium_id= int(data[3])
            cursor = connection.execute("select * from " + prefix + "media where id=" + str(medium_id))
            for item in cursor:
                release_id =int(item[1])
                params = (release_id,recording_id)
                connection.execute("update " + prefix + "recording set release_id=? where id=?" ,params)
                if i % 10000 == 0 :
                    print('musicbrainz_recording_release\t' + str(i))
        except:
            with open('error.txt','at',encoding='utf-8') as f:
                f.write('musicbrainz_recording_release\t' +str(i) + '\t' +line)
                print('musicbrainz_recording_release\t' +str(i) + '\t' +line)

        i += 1

connection.commit()


# improt recording_artist
with open(mbdump_path + 'recording','rt',encoding='utf-8') as f:
    i = 1
    for line in f:
        data = line.split('\t')
        try:
            recording_id = int(data[0])
            artist_credit= int(data[3])
            cursor = connection.execute("select * from " + prefix + "artist_credit_name where artist_credit=" + str(artist_credit))
            for item in cursor:
                artist_id =int(item[2])
                params = (None,recording_id,artist_id)
                connection.execute("insert into " + prefix + "recording_artist values(?,?,?)" ,params)
                if i % 10000 == 0 :
                    print('musicbrainz_recording_artist\t' + str(i))
        except:
            with open('error.txt','at',encoding='utf-8') as f:
                f.write('musicbrainz_recording_artist\t' +str(i) + '\t' +line)
                print('musicbrainz_recording_artist\t' +str(i) + '\t' +line)
        i += 1
connection.commit()



# improt release_tag
with open(mbdump_path + 'release_label','rt',encoding='utf-8') as f:
    i = 1
    for line in f:
        data = line.split('\t')
        try:
            release_id = int(data[1])
            label_id= int(data[2])
            params = (None,release_id,label_id)
            connection.execute("insert into " + prefix + "release_tag values(?,?,?)" ,params)
            if i % 100 == 0 :
                print('musicbrainz_release_label\t' + str(i))
        except:
            with open('error.txt','at',encoding='utf-8') as f:
                f.write('musicbrainz_release_label\t' +str(i) + '\t' +line)
        i += 1

connection.commit()


# improt l_label_recording
with open(mbdump_path + 'l_label_recording','rt',encoding='utf-8') as f:
    i = 1
    for line in f:
        data = line.split('\t')
        try:
            label_id = int(data[2])
            recording_id= int(data[3])
            params = (None,recording_id,label_id)
            connection.execute("insert into " + prefix + "recording_tag values(?,?,?)" ,params)
            if i % 10000 == 0 :
                print('musicbrainz_recording_tag\t' + str(i))
        except:
            with open('error.txt','at',encoding='utf-8') as f:
                f.write('musicbrainz_recording_tag\t' +str(i) + '\t' +line)

        i += 1

connection.commit()

connection.close()  
 


        
