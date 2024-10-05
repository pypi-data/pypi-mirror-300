import requests
import urllib.parse as urlparse
from urllib.parse import urlencode
import urllib
import pyperclip


class Cuttshort:
    def __init__(self, api_key):
        while True:
            try:
                if api_key.upper() == "UD":
                    ak = "b9fbdde0736d2ca0ad6b910bd6e60dea"
                else:
                    ak = api_key
                api_url = 'http://cutt.ly/api/api.php?key={}'.format(ak)
                data = requests.get(api_url).json()
                if data["auth"]==True:
                    while True:
                        try:
                            link = input("Enter the link to be shortened: ")
                            params = {'utm_source':'apidevthe'}
                    

                            if link.startswith("http"):
                                response = requests.head(link)
                                status = response.status_code
                                response11 = requests.get(link)
                                status11 = response11.status_code
                                url_parts = list(urlparse.urlparse(link+"/"))
                                query = dict(urlparse.parse_qsl(url_parts[4]))
                                query.update(params)
     
                                url_parts[4] = urlencode(query)
                                url1 = urlparse.urlunparse(url_parts)
                                url = urllib.parse.quote(url1)

                                if status==200:
                                    while True:
                                        name = input("Would you like to give a name? : ")
                                        if name.upper()=="YES":
                                            while True:
                                                name1 = input("Enter name: ")
                                                api_url1 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url, name1)
                                                data1 = requests.get(api_url1).json()["url"]
                                                if data1["status"] == 7:
                                                    shortened_url1 = data1["shortLink"]
                                                    print("Shortened URL: ", shortened_url1)
                                                    pyperclip.copy(shortened_url1)
                                                    break
                                                elif data1["status"] == 5:
                                                    print("Please re-enter the name as the name contains invalid characters!")
                                                else:
                                                    print("Please re-enter the name as the entered name already exists!")
                                                    continue
                                            break
                                        elif name.upper()=="NO":
                                            api_url2 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url)
                                            data2 = requests.get(api_url2).json()["url"]
                                            if data2["status"] == 7:
                                                shortened_url2 = data2["shortLink"]
                                                print("Shortened URL: ", shortened_url2)
                                                pyperclip.copy(shortened_url2)
                                                break
                                        else:
                                            print("Please enter either Yes/No!")
                                elif status==301:
                                    secpro, urllink = link.split("://")
                                    if not link.endswith("/"):
                                                link8 = link + "/"
                                                response6 = requests.head(link8)
                                                status6 = response6.status_code
                                                url_parts6 = list(urlparse.urlparse(link8))
                                                query6 = dict(urlparse.parse_qsl(url_parts6[4]))
                                                query6.update(params)
     
                                                url_parts6[4] = urlencode(query6)
                                                url12= urlparse.urlunparse(url_parts6)
                                                url13 = urllib.parse.quote(url12)

                                                if status6==200:
                                                    while True:
                                                        name12 = input("Would you like to give a name? : ")
                                                        if name12.upper()=="YES":
                                                            while True:
                                                                name13 = input("Enter name: ")
                                                                api_url13 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url13, name13)
                                                                data13 = requests.get(api_url13).json()["url"]
                                                                if data13["status"] == 7:
                                                                    shortened_url13 = data13["shortLink"]
                                                                    print("Shortened URL: ", shortened_url13)
                                                                    pyperclip.copy(shortened_url13)
                                                                    break
                                                                elif data11["status"] == 5:
                                                                    print("Please re-enter the name as the name contains invalid characters!")
                                                                else:
                                                                    print("Please re-enter the name as name already exists!")
                                                                    continue
                                                            break
                                                        elif name12.upper()=="NO":
                                                            api_url14 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url13)
                                                            data14 = requests.get(api_url14).json()["url"]
                                                            if data14["status"] == 7:
                                                                shortened_url14 = data14["shortLink"]
                                                                print("Shortened URL: ", shortened_url14)
                                                                pyperclip.copy(shortened_url14)
                                                                break
                                                        else:
                                                            print("Please enter either Yes/No!")
                                                elif status6==301:
                                                    if secpro=="http":
                                                        link41 = "https://" + urllink + "/"
                                                        response21 = requests.head(link41)
                                                        status21 = response21.status_code
                                                        url_parts21 = list(urlparse.urlparse(link41))
                                                        query21 = dict(urlparse.parse_qsl(url_parts21[4]))
                                                        query21.update(params)
     
                                                        url_parts21[4] = urlencode(query21)
                                                        url41 = urlparse.urlunparse(url_parts21)
                                                        url51 = urllib.parse.quote(url41)

                                                        if status21==200:
                                                            while True:
                                                                name41 = input("Would you like to give a name? : ")
                                                                if name41.upper()=="YES":
                                                                    while True:
                                                                        name51 = input("Enter name: ")
                                                                        api_url51 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url51, name51)
                                                                        data51 = requests.get(api_url51).json()["url"]
                                                                        if data51["status"] == 7:
                                                                            shortened_url51 = data51["shortLink"]
                                                                            print("Shortened URL: ", shortened_url51)
                                                                            pyperclip.copy(shortened_url51)
                                                                            break
                                                                        elif data51["status"] == 5:
                                                                            print("Please re-enter the name as the name contains invalid characters!")
                                                                        else:
                                                                            print("Please re-enter the name as name already exists!")
                                                                            continue
                                                                    break
                                                                elif name41.upper()=="NO":
                                                                    api_url61 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url51)
                                                                    data61 = requests.get(api_url61).json()["url"]
                                                                    if data61["status"] == 7:
                                                                        shortened_url61 = data61["shortLink"]
                                                                        print("Shortened URL: ", shortened_url61)
                                                                        pyperclip.copy(shortened_url61)
                                                                        break
                                                                else:
                                                                    print("Please enter either Yes/No!")
                                                        elif status == 301 and not link.startswith("http://www"):
                                                            link2000 = "http://www." + urllink + "/"
                                                            print(link2000)
                                                            response2000 = requests.head(link2000)
                                                            status2000 = response2000.status_code
                                                            url_parts2000 = list(urlparse.urlparse(link2000))
                                                            query2000 = dict(urlparse.parse_qsl(url_parts2000[4]))
                                                            query2000.update(params)
     
                                                            url_parts2000[4] = urlencode(query2000)
                                                            url2000 = urlparse.urlunparse(url_parts2000)
                                                            url20000 = urllib.parse.quote(url2000)
                                                            link2001 = "https://www." + urllink + "/"
                                                            response2001 = requests.head(link2001)
                                                            status2001 = response2001.status_code
                                                            print(status2001)
                                                            url_parts2001 = list(urlparse.urlparse(link2001))
                                                            query2001 = dict(urlparse.parse_qsl(url_parts2001[4]))
                                                            query2001.update(params)
     
                                                            url_parts2001[4] = urlencode(query2001)
                                                            url2001 = urlparse.urlunparse(url_parts2001)
                                                            url20001 = urllib.parse.quote(url2001)
                                                            if status2000==200:
                                                                while True:
                                                                    name2000 = input("Would you like to give a name? : ")
                                                                    if name2000.upper()=="YES":
                                                                        while True:
                                                                            name20000 = input("Enter name: ")
                                                                            api_url2000 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url20000, name20000)
                                                                            data2000 = requests.get(api_url2000).json()["url"]
                                                                            if data2000["status"] == 7:
                                                                                shortened_url2000 = data2000["shortLink"]
                                                                                print("Shortened URL: ", shortened_url2000)
                                                                                pyperclip.copy(shortened_url2000)
                                                                                break
                                                                            elif data2000["status"] == 5:
                                                                                print("Please re-enter the name as the name contains invalid characters!")
                                                                            else:
                                                                                print("Please re-enter the name as name already exists!")
                                                                                continue
                                                                        break
                                                                    elif name2000.upper()=="NO":
                                                                        api_url2001 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url20000)
                                                                        data2001 = requests.get(api_url2001).json()["url"]
                                                                        if data2001["status"] == 7:
                                                                            shortened_url2001 = data2001["shortLink"]
                                                                            print("Shortened URL: ", shortened_url2001)
                                                                            pyperclip.copy(shortened_url2001)
                                                                            break
                                                                    else:
                                                                        print("Please enter either Yes/No!")
                                                            elif status2001==200:
                                                                while True:
                                                                    name2002 = input("Would you like to give a name? : ")
                                                                    if name2002.upper()=="YES":
                                                                        while True:
                                                                            name20001 = input("Enter name: ")
                                                                            api_url2002 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url20001, name20001)
                                                                            data2002 = requests.get(api_url2002).json()["url"]
                                                                            if data2002["status"] == 7:
                                                                                shortened_url2002 = data2002["shortLink"]
                                                                                print("Shortened URL: ", shortened_url2002)
                                                                                pyperclip.copy(shortened_url2002)
                                                                                break
                                                                            elif data2002["status"] == 5:
                                                                                print("Please re-enter the name as the name contains invalid characters!")
                                                                            else:
                                                                                print("Please re-enter the name as name already exists!")
                                                                                continue
                                                                        break
                                                                    elif name2002.upper()=="NO":
                                                                        api_url2001 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url20001)
                                                                        data2001 = requests.get(api_url2001).json()["url"]
                                                                        if data2001["status"] == 7:
                                                                            shortened_url2001 = data2001["shortLink"]
                                                                            print("Shortened URL: ", shortened_url2001)
                                                                            pyperclip.copy(shortened_url2001)
                                                                            break
                                                                    else:
                                                                        print("Please enter either Yes/No!")
                                                            else:
                                                                print("The entered URL is already shortened")
                                                        else:
                                                            print("The entered URL is already shortened")
                                                    elif secpro=="https":
                                                        link42 = "http://" + urllink + "/"
                                                        response22 = requests.head(link42)
                                                        status22 = response22.status_code
                                                        url_parts22 = list(urlparse.urlparse(link42))
                                                        query22 = dict(urlparse.parse_qsl(url_parts22[4]))
                                                        query22.update(params)
     
                                                        url_parts22[4] = urlencode(query22)
                                                        url42 = urlparse.urlunparse(url_parts22)
                                                        url52 = urllib.parse.quote(url42)

                                                        if status22==200:
                                                            while True:
                                                                name42 = input("Would you like to give a name? : ")
                                                                if name42.upper()=="YES":
                                                                    while True:
                                                                        name52 = input("Enter name: ")
                                                                        api_url52 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url52, name52)
                                                                        data52 = requests.get(api_url52).json()["url"]
                                                                        if data52["status"] == 7:
                                                                            shortened_url52 = data52["shortLink"]
                                                                            print("Shortened URL: ", shortened_url52)
                                                                            pyperclip.copy(shortened_url52)
                                                                            break
                                                                        elif data52["status"] == 5:
                                                                             print("Please re-enter the name as the name contains invalid characters!")
                                                                        else:
                                                                            print("Please re-enter the name as name already exists!")
                                                                            continue
                                                                    break
                                                                elif name42.upper()=="NO":
                                                                    api_url62 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url52)
                                                                    data62 = requests.get(api_url62).json()["url"]
                                                                    if data62["status"] == 7:
                                                                        shortened_url62 = data62["shortLink"]
                                                                        print("Shortened URL: ", shortened_url62)
                                                                        pyperclip.copy(shortened_url62)
                                                                        break
                                                                else:
                                                                    print("Please enter either Yes/No!")
                                                                    continue
                                                        elif status == 301 and not link.startswith("http://www"):
                                                            link20001 = "https://www." + urllink + "/"
                                                            response20001 = requests.head(link20001)
                                                            status20001 = response20001.status_code
                                                            url_parts20001 = list(urlparse.urlparse(link20001))
                                                            query20001 = dict(urlparse.parse_qsl(url_parts20001[4]))
                                                            query20001.update(params)
     
                                                            url_parts20001[4] = urlencode(query20001)
                                                            url200001 = urlparse.urlunparse(url_parts20001)
                                                            url200002 = urllib.parse.quote(url200001)
                                                            link20011 = "http://www." + urllink + "/"
                                                            response20011 = requests.head(link20011)
                                                            status20011 = response20011.status_code
                                                            url_parts20011 = list(urlparse.urlparse(link20011))
                                                            query20011 = dict(urlparse.parse_qsl(url_parts20011[4]))
                                                            query20011.update(params)
     
                                                            url_parts20011[4] = urlencode(query20011)
                                                            url20011 = urlparse.urlunparse(url_parts20011)
                                                            url200011 = urllib.parse.quote(url20011)
                                                            if status20001==200:
                                                                while True:
                                                                    name200011 = input("Would you like to give a name? : ")
                                                                    if name200011.upper()=="YES":
                                                                        while True:
                                                                            name200001 = input("Enter name: ")
                                                                            api_url20001 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url200002, name200001)
                                                                            data20001 = requests.get(api_url20001).json()["url"]
                                                                            if data20001["status"] == 7:
                                                                                shortened_url20001 = data20001["shortLink"]
                                                                                print("Shortened URL: ", shortened_url20001)
                                                                                pyperclip.copy(shortened_url20001)
                                                                                break
                                                                            elif data20001["status"] == 5:
                                                                                print("Please re-enter the name as the name contains invalid characters!")
                                                                            else:
                                                                                print("Please re-enter the name as name already exists!")
                                                                                continue
                                                                        break
                                                                    elif name200011.upper()=="NO":
                                                                        api_url20011 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url200002)
                                                                        data20011 = requests.get(api_url20011).json()["url"]
                                                                        if data20011["status"] == 7:
                                                                            shortened_url20011 = data20011["shortLink"]
                                                                            print("Shortened URL: ", shortened_url20011)
                                                                            pyperclip.copy(shortened_url20011)
                                                                            break
                                                                    else:
                                                                        print("Please enter either Yes/No!")
                                                            elif status20011==200:
                                                                while True:
                                                                    name20022 = input("Would you like to give a name? : ")
                                                                    if name20022.upper()=="YES":
                                                                        while True:
                                                                            name200012 = input("Enter name: ")
                                                                            api_url20022 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url200011, name200012)
                                                                            data20022 = requests.get(api_url20022).json()["url"]
                                                                            if data20022["status"] == 7:
                                                                                shortened_url20022 = data20022["shortLink"]
                                                                                print("Shortened URL: ", shortened_url20022)
                                                                                pyperclip.copy(shortened_url20022)
                                                                                break
                                                                            elif data20022["status"] == 5:
                                                                                print("Please re-enter the name as the name contains invalid characters!")
                                                                            else:
                                                                                print("Please re-enter the name as name already exists!")
                                                                                continue
                                                                        break
                                                                    elif name20022.upper()=="NO":
                                                                        api_url20012 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url200011)
                                                                        data20012 = requests.get(api_url20012).json()["url"]
                                                                        if data20012["status"] == 7:
                                                                            shortened_url20012 = data20012["shortLink"]
                                                                            print("Shortened URL: ", shortened_url20012)
                                                                            pyperclip.copy(shortened_url20012)
                                                                            break
                                                                    else:
                                                                        print("Please enter either Yes/No!")
                                                            else:
                                                                print("The entered URL is already shortened")
                                                        else:
                                                            print("The entered URL is already shortened")
                                    elif secpro=="http":
                                        link4 = "https://" + urllink
                                        response2 = requests.head(link4)
                                        status2 = response2.status_code
                                        url_parts2 = list(urlparse.urlparse(link4))
                                        query2 = dict(urlparse.parse_qsl(url_parts2[4]))
                                        query2.update(params)
     
                                        url_parts2[4] = urlencode(query2)
                                        url4 = urlparse.urlunparse(url_parts2)
                                        url5 = urllib.parse.quote(url4)

                                        if status2==200:
                                            while True:
                                                name4 = input("Would you like to give a name? : ")
                                                if name4.upper()=="YES":
                                                    while True:
                                                        name5 = input("Enter name: ")
                                                        api_url5 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url5, name5)
                                                        data5 = requests.get(api_url5).json()["url"]
                                                        if data5["status"] == 7:
                                                            shortened_url5 = data5["shortLink"]
                                                            print("Shortened URL: ", shortened_url5)
                                                            pyperclip.copy(shortened_url5)
                                                            break
                                                        elif data5["status"] == 5:
                                                            print("Please re-enter the name as the name contains invalid characters!")
                                                        else:
                                                            print("Please re-enter the name as name already exists!")
                                                            continue
                                                    break
                                                elif name4.upper()=="NO":
                                                    api_url6 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url5)
                                                    data6 = requests.get(api_url6).json()["url"]
                                                    if data6["status"] == 7:
                                                        shortened_url6 = data6["shortLink"]
                                                        print("Shortened URL: ", shortened_url6)
                                                        pyperclip.copy(shortened_url6)
                                                        break
                                                else:
                                                    print("Please enter either Yes/No!")
                                        elif status2==301:
                                            if not link.endswith("/"):
                                                link7 = "https://" + urllink + "/"
                                                response5 = requests.head(link7)
                                                status5 = response5.status_code
                                                url_parts5 = list(urlparse.urlparse(link7))
                                                query5 = dict(urlparse.parse_qsl(url_parts5[4]))
                                                query5.update(params)
     
                                                url_parts5[4] = urlencode(query5)
                                                url10 = urlparse.urlunparse(url_parts5)
                                                url11 = urllib.parse.quote(url10)

                                                if status5==200:
                                                    while True:
                                                        name10 = input("Would you like to give a name? : ")
                                                        if name10.upper()=="YES":
                                                            while True:
                                                                name11 = input("Enter name: ")
                                                                api_url11 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url11, name11)
                                                                data11 = requests.get(api_url11).json()["url"]
                                                                if data11["status"] == 7:
                                                                    shortened_url11 = data11["shortLink"]
                                                                    print("Shortened URL: ", shortened_url11)
                                                                    pyperclip.copy(shortened_url11)
                                                                    break
                                                                elif data11["status"] == 5:
                                                                    print("Please re-enter the name as the name contains invalid characters!")
                                                                else:
                                                                    print("Please re-enter the name as name already exists!")
                                                                    continue
                                                            break
                                                        elif name4.upper()=="NO":
                                                            api_url12 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url11)
                                                            data12 = requests.get(api_url12).json()["url"]
                                                            if data12["status"] == 7:
                                                                shortened_url12 = data12["shortLink"]
                                                                print("Shortened URL: ", shortened_url12)
                                                                pyperclip.copy(shortened_url12)
                                                                break
                                                        else:
                                                            print("Please enter either Yes/No!")
                                            elif not link.startswith("http://www"):
                                                            link200011 = "http://www." + urllink
                                                            response200011 = requests.head(link200011)
                                                            status200011 = response200011.status_code
                                                            url_parts200011 = list(urlparse.urlparse(link200011))
                                                            query200011 = dict(urlparse.parse_qsl(url_parts200011[4]))
                                                            query200011.update(params)
     
                                                            url_parts200011[4] = urlencode(query200011)
                                                            url200011 = urlparse.urlunparse(url_parts200011)
                                                            url2000011 = urllib.parse.quote(url200011)
                                                            link200111 = "https://www." + urllink
                                                            response200111 = requests.head(link200111)
                                                            status200111 = response200111.status_code
                                                            print(status200111)
                                                            url_parts200111 = list(urlparse.urlparse(link200111))
                                                            query200111 = dict(urlparse.parse_qsl(url_parts200111[4]))
                                                            query200111.update(params)
     
                                                            url_parts200111[4] = urlencode(query200111)
                                                            url200111 = urlparse.urlunparse(url_parts200111)
                                                            url2000111 = urllib.parse.quote(url200111)
                                                            if status200011==200:
                                                                while True:
                                                                    name2000111 = input("Would you like to give a name? : ")
                                                                    if name2000111.upper()=="YES":
                                                                        while True:
                                                                            name20000111 = input("Enter name: ")
                                                                            api_url2000111 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url2000011, name20000111)
                                                                            data2000111 = requests.get(api_url2000111).json()["url"]
                                                                            if data2000111["status"] == 7:
                                                                                shortened_url2000111 = data2000111["shortLink"]
                                                                                print("Shortened URL: ", shortened_url2000111)
                                                                                pyperclip.copy(shortened_url2000111)
                                                                                break
                                                                            elif data2000111["status"] == 5:
                                                                                print("Please re-enter the name as the name contains invalid characters!")
                                                                            else:
                                                                                print("Please re-enter the name as name already exists!")
                                                                                continue
                                                                        break
                                                                    elif name2000111.upper()=="NO":
                                                                        api_url2001111 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url2000011)
                                                                        data2001111 = requests.get(api_url2001111).json()["url"]
                                                                        if data2001111["status"] == 7:
                                                                            shortened_url2001111 = data2001111["shortLink"]
                                                                            print("Shortened URL: ", shortened_url2001111)
                                                                            pyperclip.copy(shortened_url2001111)
                                                                            break
                                                                    else:
                                                                        print("Please enter either Yes/No!")
                                                            elif status200111==200:
                                                                while True:
                                                                    name200211 = input("Would you like to give a name? : ")
                                                                    if name200211.upper()=="YES":
                                                                        while True:
                                                                            name20001111 = input("Enter name: ")
                                                                            api_url2002111 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url2000111, name20001111)
                                                                            data2002111 = requests.get(api_url2002111).json()["url"]
                                                                            if data2002111["status"] == 7:
                                                                                shortened_url2002111 = data2002111["shortLink"]
                                                                                print("Shortened URL: ", shortened_url2002111)
                                                                                pyperclip.copy(shortened_url2002111)
                                                                                break
                                                                            elif data2002111["status"] == 5:
                                                                                print("Please re-enter the name as the name contains invalid characters!")
                                                                            else:
                                                                                print("Please re-enter the name as name already exists!")
                                                                                continue
                                                                        break
                                                                    elif name200211.upper()=="NO":
                                                                        api_url2001112 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url2000111)
                                                                        data2001112 = requests.get(api_url2001112).json()["url"]
                                                                        if data2001112["status"] == 7:
                                                                            shortened_url2001112 = data2001112["shortLink"]
                                                                            print("Shortened URL: ", shortened_url2001112)
                                                                            pyperclip.copy(shortened_url2001112)
                                                                            break
                                                                    else:
                                                                        print("Please enter either Yes/No!")
                                                            else:
                                                                print("The entered URL is already shortened")
                                            else:
                                                print("The entered URL is already shortened")
                                    elif secpro=="https":
                                        link5 = "http://" + urllink
                                        response3 = requests.head(link5)
                                        status3 = response3.status_code
                                        url_parts3 = list(urlparse.urlparse(link5))
                                        query3 = dict(urlparse.parse_qsl(url_parts3[4]))
                                        query3.update(params)
     
                                        url_parts3[4] = urlencode(query3)
                                        url6 = urlparse.urlunparse(url_parts3)
                                        url7 = urllib.parse.quote(url6)

                                        if status3==200:
                                            while True:
                                                name6 = input("Would you like to give a name? : ")
                                                if name6.upper()=="YES":
                                                    while True:
                                                        name7 = input("Enter name: ")
                                                        api_url7 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url7, name7)
                                                        data7 = requests.get(api_url7).json()["url"]
                                                        if data7["status"] == 7:
                                                            shortened_url7 = data7["shortLink"]
                                                            print("Shortened URL: ", shortened_url7)
                                                            pyperclip.copy(shortened_url7)
                                                            break
                                                        elif data7["status"] == 5:
                                                            print("Please re-enter the name as the name contains invalid characters!")
                                                        else:
                                                            print("Please re-enter the name as name already exists!")
                                                            continue
                                                    break
                                                elif name6.upper()=="NO":
                                                    api_url8 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url7)
                                                    data8 = requests.get(api_url8).json()["url"]
                                                    if data8["status"] == 7:
                                                        shortened_url8 = data8["shortLink"]
                                                        print("Shortened URL: ", shortened_url8)
                                                        pyperclip.copy(shortened_url8)
                                                        break
                                                else:
                                                    print("Please enter either Yes/No!")
                                        elif status3==301:
                                            if not link.endswith("/"):
                                                link7 = "https://" + urllink + "/"
                                                response5 = requests.head(link7)
                                                status5 = response5.status_code
                                                url_parts5 = list(urlparse.urlparse(link7))
                                                query5 = dict(urlparse.parse_qsl(url_parts5[4]))
                                                query5.update(params)
     
                                                url_parts5[4] = urlencode(query5)
                                                url10 = urlparse.urlunparse(url_parts5)
                                                url11 = urllib.parse.quote(url10)

                                                if status5==200:
                                                    while True:
                                                        name10 = input("Would you like to give a name? : ")
                                                        if name10.upper()=="YES":
                                                            while True:
                                                                name11 = input("Enter name: ")
                                                                api_url11 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url11, name11)
                                                                data11 = requests.get(api_url11).json()["url"]
                                                                if data11["status"] == 7:
                                                                    shortened_url11 = data11["shortLink"]
                                                                    print("Shortened URL: ", shortened_url11)
                                                                    pyperclip.copy(shortened_url11)
                                                                    break
                                                                elif data11["status"] == 5:
                                                                    print("Please re-enter the name as the name contains invalid characters!")
                                                                else:
                                                                    print("Please re-enter the name as name already exists!")
                                                                    continue
                                                            break
                                                        elif name4.upper()=="NO":
                                                            api_url12 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url11)
                                                            data12 = requests.get(api_url12).json()["url"]
                                                            if data12["status"] == 7:
                                                                shortened_url12 = data12["shortLink"]
                                                                print("Shortened URL: ", shortened_url12)
                                                                pyperclip.copy(shortened_url12)
                                                                break
                                                        else:
                                                            print("Please enter either Yes/No!")
                                            elif not link.startswith("https://www"):
                                                            link2000111 = "https://www." + urllink
                                                            response2000111 = requests.head(link2000111)
                                                            status2000111 = response2000111.status_code
                                                            url_parts2000111 = list(urlparse.urlparse(link2000111))
                                                            query2000111 = dict(urlparse.parse_qsl(url_parts2000111[4]))
                                                            query2000111.update(params)
     
                                                            url_parts2000111[4] = urlencode(query2000111)
                                                            url20001111 = urlparse.urlunparse(url_parts2000111)
                                                            url20000111 = urllib.parse.quote(url20001111)
                                                            link2001111 = "http://www." + urllink
                                                            response2001111 = requests.head(link2001111)
                                                            status2001111 = response2001111.status_code
                                                            url_parts2001111 = list(urlparse.urlparse(link2001111))
                                                            query2001111 = dict(urlparse.parse_qsl(url_parts2001111[4]))
                                                            query2001111.update(params)
     
                                                            url_parts2001111[4] = urlencode(query2001111)
                                                            url2001111 = urlparse.urlunparse(url_parts2001111)
                                                            url200011111 = urllib.parse.quote(url2001111)
                                                            if status2000111==200:
                                                                while True:
                                                                    name200011111 = input("Would you like to give a name? : ")
                                                                    if name200011111.upper()=="YES":
                                                                        while True:
                                                                            name200001111 = input("Enter name: ")
                                                                            api_url20001111 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url20000111, name200001111)
                                                                            data20001111 = requests.get(api_url20001111).json()["url"]
                                                                            if data20001111["status"] == 7:
                                                                                shortened_url20001111 = data20001111["shortLink"]
                                                                                print("Shortened URL: ", shortened_url20001111)
                                                                                pyperclip.copy(shortened_url20001111)
                                                                                break
                                                                            elif data20001111["status"] == 5:
                                                                                print("Please re-enter the name as the name contains invalid characters!")
                                                                            else:
                                                                                print("Please re-enter the name as name already exists!")
                                                                                continue
                                                                        break
                                                                    elif name200011111.upper()=="NO":
                                                                        api_url20011111 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url20000111)
                                                                        data20011111 = requests.get(api_url20011111).json()["url"]
                                                                        if data20011111["status"] == 7:
                                                                            shortened_url20011111 = data20011111["shortLink"]
                                                                            print("Shortened URL: ", shortened_url20011111)
                                                                            pyperclip.copy(shortened_url20011111)
                                                                            break
                                                                    else:
                                                                        print("Please enter either Yes/No!")
                                                            elif status2001111==200:
                                                                while True:
                                                                    name2002111 = input("Would you like to give a name? : ")
                                                                    if name2002111.upper()=="YES":
                                                                        while True:
                                                                            name2000111111 = input("Enter name: ")
                                                                            api_url20021111 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url200011111, name2000111111)
                                                                            data20021111 = requests.get(api_url20021111).json()["url"]
                                                                            if data20021111["status"] == 7:
                                                                                shortened_url20021111 = data20021111["shortLink"]
                                                                                print("Shortened URL: ", shortened_url20021111)
                                                                                pyperclip.copy(shortened_url20021111)
                                                                                break
                                                                            elif data20021111["status"] == 5:
                                                                                print("Please re-enter the name as the name contains invalid characters!")
                                                                            else:
                                                                                print("Please re-enter the name as name already exists!")
                                                                                continue
                                                                        break
                                                                    elif name2002111.upper()=="NO":
                                                                        api_url20011122 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url200011111)
                                                                        data20011122 = requests.get(api_url20011122).json()["url"]
                                                                        if data20011122["status"] == 7:
                                                                            shortened_url20011122 = data20011122["shortLink"]
                                                                            print("Shortened URL: ", shortened_url20011122)
                                                                            pyperclip.copy(shortened_url20011122)
                                                                            break
                                                                    else:
                                                                        print("Please enter either Yes/No!")
                                                            else:
                                                                print("The entered URL is already shortened")
                                        else:
                                            print("The entered URL is already shortened")
                                    else:
                                            print("The entered URL is already shortened")
                                elif status == 302 and status11 == 200:
                                    secpro111, urllink111 = link.split("://")
                                    if secpro111 == "http":
                                        link6111 = "https://" + urllink111
                                        response411 = requests.head(link6111)
                                        status411 = response411.status_code
                                        link611111 = "https://" + urllink111 + "/"
                                        response4111 = requests.head(link611111)
                                        status4111 = response4111.status_code
                                        url_parts4111 = list(urlparse.urlparse(link611111))
                                        query4111 = dict(urlparse.parse_qsl(url_parts4111[4]))
                                        query4111.update(params)
     
                                        url_parts4111[4] = urlencode(query4111)
                                        url8111 = urlparse.urlunparse(url_parts4111)
                                        url9111 = urllib.parse.quote(url8111)
                                        l = [link]

                                        for i in l:
                                            try:
                                                link61111 = requests.head(i).headers["location"]
                                                print (link61111)
                                                link611111 = link6111 + "/"
                                                print(link611111)
                                                if link6111 == link61111 or link611111:
                                                    while True:
                                                        name1411 = input("Would you like to give a name? : ")
                                                        if name1411.upper()=="YES":
                                                            while True:
                                                                name1511 = input("Enter name: ")
                                                                api_url1511 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url9111, name1511)
                                                                data1511 = requests.get(api_url1511).json()["url"]
                                                                if data1511["status"] == 7:
                                                                    shortened_url1511 = data1511["shortLink"]
                                                                    print("Shortened URL: ", shortened_url1511)
                                                                    pyperclip.copy(shortened_url1511)
                                                                    break
                                                                elif data1511["status"] == 5:
                                                                    print("Please re-enter the name as the name contains invalid characters!")
                                                                else:
                                                                    print("Please re-enter the name as name already exists!")
                                                                    continue
                                                            break
                                                        elif name1411.upper()=="NO":
                                                            api_url1611 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url9111)
                                                            data1611 = requests.get(api_url1611).json()["url"]
                                                            if data1611["status"] == 7:
                                                                shortened_url1611 = data1611["shortLink"]
                                                                print("Shortened URL: ", shortened_url1611)
                                                                pyperclip.copy(shortened_url1611)
                                                            break
                                                        else:
                                                            print("Please enter either Yes/No!")
                                            except KeyError as exception:
                                                while True:
                                                    name1421 = input("Would you like to give a name? : ")
                                                    if name1421.upper()=="YES":
                                                        while True:
                                                            name1521 = input("Enter name: ")
                                                            api_url1521 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url, name1521)
                                                            data1521 = requests.get(api_url1521).json()["url"]
                                                            if data1521["status"] == 7:
                                                                shortened_url1521 = data1521["shortLink"]
                                                                print("Shortened URL: ", shortened_url1521)
                                                                pyperclip.copy(shortened_url1521)
                                                                break
                                                            elif data1521["status"] == 5:
                                                                print("Please re-enter the name as the name contains invalid characters!")
                                                            else:
                                                                print("Please re-enter the name as name already exists!")
                                                                continue
                                                        break
                                                    elif name1421.upper()=="NO":
                                                        api_url1621 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url)
                                                        data1621 = requests.get(api_url1621).json()["url"]
                                                        if data1621["status"] == 7:
                                                            shortened_url1621 = data1621["shortLink"]
                                                            print("Shortened URL: ", shortened_url1621)
                                                            pyperclip.copy(shortened_url1621)
                                                            break
                                                    else:
                                                        print("Please enter either Yes/No!")
                                    if secpro111 == "https":
                                        link6112 = "http://" + urllink111
                                        response412 = requests.head(link6112)
                                        status412 = response412.status_code
                                        url_parts412 = list(urlparse.urlparse(link6112))
                                        query412 = dict(urlparse.parse_qsl(url_parts412[4]))
                                        query412.update(params)
     
                                        url_parts412[4] = urlencode(query412)
                                        url812 = urlparse.urlunparse(url_parts412)
                                        url912 = urllib.parse.quote(url812)
                                        l = [link]

                                        for i in l:
                                            try:
                                                link61112 = requests.head(i).headers["location"]
                                                print (link61112)
                                                link611112 = link6112 + "/"
                                                print(link611112)
                                                if link6112 == link61112 or link611112:
                                                    while True:
                                                        name1412 = input("Would you like to give a name? : ")
                                                        if name1412.upper()=="YES":
                                                            while True:
                                                                name1512 = input("Enter name: ")
                                                                api_url1512 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url912, name1512)
                                                                data1512 = requests.get(api_url1512).json()["url"]
                                                                if data1512["status"] == 7:
                                                                    shortened_url1512 = data1512["shortLink"]
                                                                    print("Shortened URL: ", shortened_url1512)
                                                                    pyperclip.copy(shortened_url1512)
                                                                    break
                                                                elif data1512["status"] == 5:
                                                                    print("Please re-enter the name as the name contains invalid characters!")
                                                                else:
                                                                    print("Please re-enter the name as name already exists!")
                                                                    continue
                                                            break
                                                        elif name142.upper()=="NO":
                                                            api_url1612 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url912)
                                                            data1612 = requests.get(api_url1612).json()["url"]
                                                            if data1612["status"] == 7:
                                                                shortened_url1612 = data1612["shortLink"]
                                                                print("Shortened URL: ", shortened_url1612)
                                                                pyperclip.copy(shortened_url1612)
                                                            break
                                                        else:
                                                            print("Please enter either Yes/No!")
                                            except KeyError as exception:
                                                while True:
                                                    name1422 = input("Would you like to give a name? : ")
                                                    if name1422.upper()=="YES":
                                                        while True:
                                                            name1522 = input("Enter name: ")
                                                            api_url1522 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url, name1522)
                                                            data1522 = requests.get(api_url1522).json()["url"]
                                                            if data1522["status"] == 7:
                                                                shortened_url1522 = data1522["shortLink"]
                                                                print("Shortened URL: ", shortened_url1522)
                                                                pyperclip.copy(shortened_url1522)
                                                                break
                                                            elif data1522["status"] == 5:
                                                                print("Please re-enter the name as the name contains invalid characters!")
                                                            else:
                                                                print("Please re-enter the name as name already exists!")
                                                                continue
                                                        break
                                                    elif name1422.upper()=="NO":
                                                        api_url1622 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url)
                                                        data1622 = requests.get(api_url1622).json()["url"]
                                                        if data1622["status"] == 7:
                                                            shortened_url1622 = data1622["shortLink"]
                                                            print("Shortened URL: ", shortened_url1622)
                                                            pyperclip.copy(shortened_url1622)
                                                            break
                                                    else:
                                                        print("Please enter either Yes/No!")
                                else:
                                    print("URL does not exist on the Internet")
                            else:
                                link1 = "http://" + link
                                response1 = requests.head(link1)
                                status1 = response1.status_code
                                response12 = requests.get(link1)
                                status12 = response12.status_code
                                url_parts1 = list(urlparse.urlparse(link1))
                                query1 = dict(urlparse.parse_qsl(url_parts1[4]))
                                query1.update(params)
     
                                url_parts1[4] = urlencode(query1)
                                url2 = urlparse.urlunparse(url_parts1)
                                url3 = urllib.parse.quote(url2)
                                if status1 == 200:
                                    while True:
                                        name3 = input("Would you like to give a name? : ")
                                        if name3.upper()=="YES":
                                            while True:
                                                name2 = input("Enter name: ")
                                                api_url3 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url3, name2)
                                                data3 = requests.get(api_url3).json()["url"]
                                                if data3["status"] == 7:
                                                    shortened_url3 = data3["shortLink"]
                                                    print("Shortened URL: ", shortened_url3)
                                                    pyperclip.copy(shortened_url3)
                                                    break
                                                elif data3["status"] == 5:
                                                    print("Please re-enter the name as the name contains invalid characters!")
                                                else:
                                                    print("Please re-enter the name as name already exists!")
                                                    continue
                                            break
                                        elif name3.upper()=="NO":
                                            api_url4 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url3)
                                            data4 = requests.get(api_url4).json()["url"]
                                            if data4["status"] == 7:
                                                shortened_url4 = data4["shortLink"]
                                                print("Shortened URL: ", shortened_url4)
                                                pyperclip.copy(shortened_url4)
                                                break
                                        else:
                                            print("Please enter either Yes/No!")
                                elif status1 == 301:
                                    secpro1, urllink1 = link1.split("://")
                                    link6 = "https://" + urllink1 + "/"
                                    response4 = requests.head(link6)
                                    status4 = response4.status_code
                                    url_parts4 = list(urlparse.urlparse(link6))
                                    query4 = dict(urlparse.parse_qsl(url_parts4[4]))
                                    query4.update(params)
     
                                    url_parts4[4] = urlencode(query4)
                                    url8 = urlparse.urlunparse(url_parts4)
                                    url9 = urllib.parse.quote(url8)

                                    if status4==200:
                                        while True:
                                            name8 = input("Would you like to give a name? : ")
                                            if name8.upper()=="YES":
                                                while True:
                                                    name9 = input("Enter name: ")
                                                    api_url9 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url9, name9)
                                                    data9 = requests.get(api_url9).json()["url"]
                                                    if data9["status"] == 7:
                                                        shortened_url9  = data9["shortLink"]
                                                        print("Shortened URL: ", shortened_url9)
                                                        pyperclip.copy(shortened_url9)
                                                        break
                                                    elif data9["status"] == 5:
                                                        print("Please re-enter the name as the name contains invalid characters!")
                                                    else:
                                                        print("Please re-enter the name as name already exists!")
                                                        continue
                                                break
                                            elif name8.upper()=="NO":
                                                api_url10 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url9)
                                                data10 = requests.get(api_url10).json()["url"]
                                                if data10["status"] == 7:
                                                    shortened_url10 = data10["shortLink"]
                                                    print("Shortened URL: ", shortened_url10)
                                                    pyperclip.copy(shortened_url10)
                                                    break
                                            else:
                                                print("Please enter either Yes/No!")
                                                continue
                                    elif status4==301:
                                        if not link.endswith("/"):
                                            link9 = link6 + "/"
                                            response7 = requests.head(link9)
                                            status7 = response7.status_code
                                            url_parts7 = list(urlparse.urlparse(link9))
                                            query7 = dict(urlparse.parse_qsl(url_parts7[4]))
                                            query7.update(params)
     
                                            url_parts7[4] = urlencode(query7)
                                            url14 = urlparse.urlunparse(url_parts7)
                                            url15 = urllib.parse.quote(url14)

                                            if status7==200:
                                                while True:
                                                    name14 = input("Would you like to give a name? : ")
                                                    if name14.upper()=="YES":
                                                        while True:
                                                            name15 = input("Enter name: ")
                                                            api_url15 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url15, name15)
                                                            data15 = requests.get(api_url15).json()["url"]
                                                            if data15["status"] == 7:
                                                                shortened_url15 = data15["shortLink"]
                                                                print("Shortened URL: ", shortened_url15)
                                                                pyperclip.copy(shortened_url15)
                                                                break
                                                            elif data15["status"] == 5:
                                                                print("Please re-enter the name as the name contains invalid characters!")
                                                            else:
                                                                print("Please re-enter the name as name already exists!")
                                                                continue
                                                        break
                                                    elif name14.upper()=="NO":
                                                        api_url16 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url15)
                                                        data16 = requests.get(api_url16).json()["url"]
                                                        if data16["status"] == 7:
                                                            shortened_url16 = data16["shortLink"]
                                                            print("Shortened URL: ", shortened_url16)
                                                            pyperclip.copy(shortened_url16)
                                                            break
                                                    else:
                                                        print("Please enter either Yes/No!")
                                            elif status7 == 301 and not link.startswith("http://www"):
                                                            link2000200 = "http://www." + urllink1 + "/"
                                                            response2000200 = requests.head(link2000200)
                                                            status2000200 = response2000200.status_code
                                                            url_parts2000200 = list(urlparse.urlparse(link2000200))
                                                            query2000200 = dict(urlparse.parse_qsl(url_parts2000200[4]))
                                                            query2000200.update(params)
     
                                                            url_parts2000200[4] = urlencode(query2000200)
                                                            url2000200 = urlparse.urlunparse(url_parts2000200)
                                                            url20000200 = urllib.parse.quote(url2000200)
                                                            link2001200 = "https://www." + urllink1 + "/"
                                                            response2001200 = requests.head(link2001200)
                                                            status2001200 = response2001200.status_code
                                                            url_parts2001200 = list(urlparse.urlparse(link2001200))
                                                            query2001200 = dict(urlparse.parse_qsl(url_parts2001200[4]))
                                                            query2001200.update(params)
     
                                                            url_parts2001200[4] = urlencode(query2001200)
                                                            url2001200 = urlparse.urlunparse(url_parts2001200)
                                                            url20001200 = urllib.parse.quote(url2001200)
                                                            if status2000200==200:
                                                                while True:
                                                                    name2000200 = input("Would you like to give a name? : ")
                                                                    if name2000200.upper()=="YES":
                                                                        while True:
                                                                            name20000200 = input("Enter name: ")
                                                                            api_url2000200 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url20000200, name20000200)
                                                                            data2000200 = requests.get(api_url2000200).json()["url"]
                                                                            if data2000200["status"] == 7:
                                                                                shortened_url2000200 = data2000200["shortLink"]
                                                                                print("Shortened URL: ", shortened_url2000200)
                                                                                pyperclip.copy(shortened_url2000200)
                                                                                break
                                                                            elif data2000200["status"] == 5:
                                                                                print("Please re-enter the name as the name contains invalid characters!")
                                                                            else:
                                                                                print("Please re-enter the name as name already exists!")
                                                                                continue
                                                                        break
                                                                    elif name2000200.upper()=="NO":
                                                                        api_url2001200 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url20000200)
                                                                        data2001200 = requests.get(api_url2001200).json()["url"]
                                                                        if data2001200["status"] == 7:
                                                                            shortened_url2001200 = data2001200["shortLink"]
                                                                            print("Shortened URL: ", shortened_url2001200)
                                                                            pyperclip.copy(shortened_url2001200)
                                                                            break
                                                                    else:
                                                                        print("Please enter either Yes/No!")
                                                            elif status2001200==200:
                                                                while True:
                                                                    name2002200 = input("Would you like to give a name? : ")
                                                                    if name2002200.upper()=="YES":
                                                                        while True:
                                                                            name20001200 = input("Enter name: ")
                                                                            api_url2002200 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url20001200, name20001200)
                                                                            data2002200 = requests.get(api_url2002200).json()["url"]
                                                                            if data2002200["status"] == 7:
                                                                                shortened_url2002200 = data2002200["shortLink"]
                                                                                print("Shortened URL: ", shortened_url2002200)
                                                                                pyperclip.copy(shortened_url2002200)
                                                                                break
                                                                            elif data2002200["status"] == 5:
                                                                                print("Please re-enter the name as the name contains invalid characters!")
                                                                            else:
                                                                                print("Please re-enter the name as name already exists!")
                                                                                continue
                                                                        break
                                                                    elif name2002200.upper()=="NO":
                                                                        api_url2001200 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url20001200)
                                                                        data2001200 = requests.get(api_url2001200).json()["url"]
                                                                        if data2001200["status"] == 7:
                                                                            shortened_url2001200 = data2001200["shortLink"]
                                                                            print("Shortened URL: ", shortened_url2001200)
                                                                            pyperclip.copy(shortened_url2001200)
                                                                            break
                                                                    else:
                                                                        print("Please enter either Yes/No!")
                                                            else:
                                                                print("The entered URL is already shortened")
                                            else:
                                                print("The entered URL is already shortened")
                                elif status1==302 and status12==200:
                                    secpro11, urllink11 = link1.split("://")
                                    link61 = "https://" + urllink11
                                    response41 = requests.head(link61)
                                    status41 = response41.status_code
                                    link611122 = link61 + "/"
                                    response41112 = requests.head(link611122)
                                    status41112 = response41112.status_code
                                    url_parts41 = list(urlparse.urlparse(link611122))
                                    query41 = dict(urlparse.parse_qsl(url_parts41[4]))
                                    query41.update(params)
     
                                    url_parts41[4] = urlencode(query41)
                                    url81 = urlparse.urlunparse(url_parts41)
                                    url91 = urllib.parse.quote(url81)
                                    l = [link1]

                                    for i in l:
                                        try:
                                            link611 = requests.head(i).headers["location"]
                                            print (link611)
                                            if link611 == link611122:
                                                while True:
                                                    name141 = input("Would you like to give a name? : ")
                                                    if name141.upper()=="YES":
                                                        while True:
                                                            name151 = input("Enter name: ")
                                                            api_url151 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url91, name151)
                                                            data151 = requests.get(api_url151).json()["url"]
                                                            if data151["status"] == 7:
                                                                shortened_url151 = data151["shortLink"]
                                                                print("Shortened URL: ", shortened_url151)
                                                                pyperclip.copy(shortened_url151)
                                                                break
                                                            elif data151["status"] == 5:
                                                                print("Please re-enter the name as the name contains invalid characters!")
                                                            else:
                                                                print("Please re-enter the name as name already exists!")
                                                                continue
                                                        break
                                                    elif name141.upper()=="NO":
                                                        api_url161 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url91)
                                                        data161 = requests.get(api_url161).json()["url"]
                                                        if data161["status"] == 7:
                                                            shortened_url161 = data161["shortLink"]
                                                            print("Shortened URL: ", shortened_url161)
                                                            pyperclip.copy(shortened_url161)
                                                            break
                                                    else:
                                                        print("Please enter either Yes/No!")
                                        except KeyError as exception:
                                                while True:
                                                    name142 = input("Would you like to give a name? : ")
                                                    if name142.upper()=="YES":
                                                        while True:
                                                            name152 = input("Enter name: ")
                                                            api_url152 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url3, name152)
                                                            data152 = requests.get(api_url152).json()["url"]
                                                            if data152["status"] == 7:
                                                                shortened_url152 = data152["shortLink"]
                                                                print("Shortened URL: ", shortened_url152)
                                                                pyperclip.copy(shortened_url152)
                                                                break
                                                            elif data152["status"] == 5:
                                                                print("Please re-enter the name as the name contains invalid characters!")
                                                            else:
                                                                print("Please re-enter the name as name already exists!")
                                                                continue
                                                        break
                                                    elif name142.upper()=="NO":
                                                        api_url162 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url3)
                                                        data162 = requests.get(api_url162).json()["url"]
                                                        if data162["status"] == 7:
                                                            shortened_url162 = data162["shortLink"]
                                                            print("Shortened URL: ", shortened_url162)
                                                            pyperclip.copy(shortened_url162)
                                                            break
                                                    else:
                                                        print("Please enter either Yes/No!")
                                else:
                                    print("URL does not exist on the Internet")

                        except requests.ConnectionError as exception:
                            
                            print("URL does not exist on the Internet")
                            break
                else:
                    print("The entered API key does not exist. Please retry!")
                    break
            except requests.JSONDecodeError as exception:
                print("There is an issue with the API. Please try after a few seconds")
                break

if __name__ == "__main__":
    import stdiomask
    api_key = stdiomask.getpass("Enter your Cuttly api key: ")
    short = Cuttshort(api_key)
