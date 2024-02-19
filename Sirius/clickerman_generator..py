f = open("res.txt", "w")

def type_text(text):
    res = "WHILE(1)\n"
    res += "\t\tLCLICK(1770,1017)\n"
    res += "\t\tWAITMS(50)\n"
    for char in text:
        if char == ' ' or char == '\n' or char == '()' or char == ')':
            # print(f"char{char}:{char == ' '}")
            res += "\t\tKEYDOWN(#ENTER)\n"
            res += "\t\tWAITMS(100)\n"
            res += "\t\tKEYUP(#ENTER)\n"
            res += "\t\tWAITMS(500)\n"
            res += "\n\n"
            res += "\t\tLCLICK(1770,1017)\n"
            res += "\t\tWAITMS(5)\n"
            continue
        res += f"\t\tKEYDOWN(#{char})\n"
        res += "\t\tWAITMS(50)\n"
        res += f"\t\tKEYUP(#{char})\n"
        res += "\t\tWAITMS(50)\n"
    res += "END_CYC"
    return res

# banned = """nigger, nigga, naga, ниггер, нига, нага
#     faggot, пидор, пидорас, педик, гомик, петух (если не подразумевается птица)
#     хохол, хач, жид
#     хиджаб (в негативном контексте)
#     даун, аутист, дебил, retard
#     virgin, simp, incel, девственник, cимп, инцел
#     cunt, пизда (по отношению к девушке)
#     куколд
#     белый, натурал, гетеросексуал"""

banned = "nigger pidor daun gondon kartaviy faggot snitch virgin simp incel cunt retard naga"

# print(type_text(banned))
res = type_text(banned)
f.write(res)
f.close()
print(res)


# LCLICK(1770, 1030)
#    WAITMS(100)
#    KEYSTRING("бебра")
#    WAITMS(100)
#    KEYDOWN(#A)
#    WAITMS(100)
#    KEYUP(#A)
# 	 KEYDOWN(#ENTER)
#    WAITMS(100)
#    KEYUP(#ENTER)
#    WAITMS(100)

#    LCLICK(1770, 1030)
#    WAITMS(100)
#    KEYSTRING("бебра")
#    WAITMS(100)
#    KEYDOWN(#B)
#    WAITMS(100)
#    KEYUP(#B)
# 	 KEYDOWN(#ENTER)
#    WAITMS(100)
#    KEYUP(#ENTER)
#    WAITMS(200)

#    LCLICK(1770, 1030)
#    WAITMS(100)
#    KEYSTRING("бебра")
#    WAITMS(100)
#    KEYDOWN(#C)
#    WAITMS(100)
#    KEYUP(#C)
# 	 KEYDOWN(#ENTER)
#    WAITMS(100)
#    KEYUP(#ENTER)
#    WAITMS(300)

#    LCLICK(1770, 1030)
#    WAITMS(100)
#    KEYSTRING("бебра")
#    WAITMS(100)
#    KEYDOWN(#D)
#    WAITMS(100)
#    KEYUP(#D)
# 	 KEYDOWN(#ENTER)
#    WAITMS(100)
#    KEYUP(#ENTER)
#    WAITMS(1000)

#    LCLICK(1770, 1030)
#    WAITMS(100)
#    KEYSTRING("бебра")
#    WAITMS(100)
#    KEYDOWN(#E)
#    WAITMS(100)
#    KEYUP(#F)
# 	 KEYDOWN(#ENTER)
#    WAITMS(100)
#    KEYUP(#ENTER)
#    WAITMS(1000)

#    LCLICK(1770, 1030)
#    WAITMS(100)
#    KEYSTRING("бебра")
#    WAITMS(100)
#    KEYDOWN(#G)
#    WAITMS(100)
#    KEYUP(#G)
# 	 KEYDOWN(#ENTER)
#    WAITMS(100)
#    KEYUP(#ENTER)
#    WAITMS(400)

#    LCLICK(1770, 1030)
#    WAITMS(100)
#    KEYSTRING("бебра")
#    WAITMS(100)
#    KEYDOWN(#L)
#    WAITMS(100)
#    KEYUP(#L)
# 	 KEYDOWN(#ENTER)
#    WAITMS(100)
#    KEYUP(#ENTER)
#    WAITMS(1000)

#    LCLICK(1770, 1030)
#    WAITMS(100)
#    KEYSTRING("бебра")
#    WAITMS(100)
#    KEYDOWN(#H)
#    WAITMS(100)
#    KEYUP(#H)
# 	 KEYDOWN(#ENTER)
#    WAITMS(100)
#    KEYUP(#ENTER)
#    WAITMS(500)

#    LCLICK(1770, 1030)
#    WAITMS(100)
#    KEYSTRING("бебра")
#    WAITMS(100)
#    KEYDOWN(#F)
#    WAITMS(100)
#    KEYUP(#F)
# 	 KEYDOWN(#ENTER)
#    WAITMS(100)
#    KEYUP(#ENTER)
#    WAITMS(600)

#    LCLICK(1770, 1030)
#    WAITMS(100)
#    KEYSTRING("бебра")
#    WAITMS(100)
#    KEYDOWN(#X)
#    WAITMS(100)
#    KEYUP(#X)
# 	 KEYDOWN(#ENTER)
#    WAITMS(100)
#    KEYUP(#ENTER)
#    WAITMS(1000)

#    LCLICK(1770, 1030)
#    WAITMS(100)
#    KEYSTRING("бебра")
#    WAITMS(100)
#    KEYDOWN(#U)
#    WAITMS(100)
#    KEYUP(#U)
# 	 KEYDOWN(#ENTER)
#    WAITMS(100)
#    KEYUP(#ENTER)
#    WAITMS(700)

#    LCLICK(1770, 1030)
#    WAITMS(100)
#    KEYSTRING("бебра")
#    WAITMS(100)
#    KEYDOWN(#Y)
#    WAITMS(100)
#    KEYUP(#Y)
# 	 KEYDOWN(#ENTER)
#    WAITMS(100)
#    KEYUP(#ENTER)
#    WAITMS(800)
