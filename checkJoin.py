def check_Join(client, config): #Bunch of hacky requests stuff to get through UofT login. Returns the last page's HTML as text
    start_url = "https://apply.adm.utoronto.ca/manage/login?realm=&r=/portal/status"
    login_url = "https://idpz.utorauth.utoronto.ca/idp/profile/SAML2/Redirect/"
    nojs_forward = "https://slate.technolutions.net/manage/login"
    portal_url = "https://apply.adm.utoronto.ca/portal/status"
    login_data = {
        "j_username": config["user"],
        "j_password": config["pass"],
        "$csrfToken.getParameterName()": "$csrfToken.getToken()",
        "_eventId_proceed": "" 
    }

    nojs_data = {
        "RelayState" : "securitySlatePassthrough=1&RelayState=https%3a%2f%2fapply.adm.utoronto.ca%2fmanage%2flogin%3frealm%3d%26r%3d%2fportal%2fstatus",
        "SAMLResponse": ""
    }

    login_header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": "JSESSIONID=", #update later w/ JSESSION
        #"Host": "idpz.utorauth.utoronto.ca",
        "Origin": "https://idpz.utorauth.utoronto.ca",
        "Referer": "https://idpz.utorauth.utoronto.ca/idp/profile/SAML2/Redirect/SSO;jsessionid=", #reupdated w/ url later
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
        "Upgrade-Insecure-Requests": "1"
    }

    r = client.get(start_url)
    login_url = login_url + r.url[r.url.index("SSO"):]
    session_ID = login_url[login_url.index("jsessionid=")+11:].split("?")[0] ##hacky thing to get Session ID
    login_header["Cookie"] = login_header["Cookie"] + session_ID
    login_header["Referer"] = r.url
    client.get(r.url)
    r = client.post(login_url, data=login_data, headers=login_header)
    nojs_data["SAMLResponse"] = r.text[r.text.index('name="SAMLResponse" value="')+27:].split('"/>')[0]
    s = client.post(nojs_forward, data=nojs_data, headers=login_header)
    shit = client.post("https://apply.adm.utoronto.ca/manage/login?realm=&r=/portal/status", data={"SAMLResponse":nojs_data["SAMLResponse"]})
    client.get(portal_url)
    t = client.get("https://apply.adm.utoronto.ca/portal/status?cmd=sts")
    return t.text
