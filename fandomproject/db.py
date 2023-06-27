import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

value1 = 'https://image.genie.co.kr/Y/IMAGE/IMG_ALBUM/083/699/369/83699369_1681177236277_1_600x600.JPG/dims/resize/Q_80,0'
value2 = 'https://image.genie.co.kr/Y/IMAGE/IMG_ALBUM/083/665/559/83665559_1681116738103_1_600x600.JPG/dims/resize/Q_80,0'
value3 = 'https://image.genie.co.kr/Y/IMAGE/IMG_ALBUM/081/354/892/81354892_1580883251450_1_600x600.JPG/dims/resize/Q_80,0'
value4 = 'https://image.genie.co.kr/Y/IMAGE/IMG_ALBUM/083/779/626/83779626_1682991212396_1_600x600.JPG/dims/resize/Q_80,0'
value5 = 'https://image.genie.co.kr/Y/IMAGE/IMG_ALBUM/083/810/194/83810194_1684117368811_1_600x600.JPG/dims/resize/Q_80,0'

cursor.execute("UPDATE challenge_ref_video SET img = ? WHERE id = 1", (value1,))
cursor.execute("UPDATE challenge_ref_video SET img = ? WHERE id = 2", (value2,))
cursor.execute("UPDATE challenge_ref_video SET img = ? WHERE id = 3", (value3,))
cursor.execute("UPDATE challenge_ref_video SET img = ? WHERE id = 4", (value4,))
cursor.execute("UPDATE challenge_ref_video SET img = ? WHERE id = 5", (value5,))
# cursor.execute("DELETE FROM challenge_score WHERE id = 1")

conn.commit()
conn.close()