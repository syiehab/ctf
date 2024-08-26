# Web

## Elite
![image](https://github.com/user-attachments/assets/73de304c-794c-44f6-ba9f-614570834374)

![image](https://github.com/user-attachments/assets/58ea70fa-2c71-4210-a7c0-06e24d7e6996)

![image](https://github.com/user-attachments/assets/67bd59ba-1923-47b3-9c4c-09a21f5ff571)

![image](https://github.com/user-attachments/assets/79f62893-eda0-4fa7-a132-a50445fa55c0)

```
curl http://chall.ycfteam.in:6375/elite -H "User-Agent: Elite" -H "X-Forwarded-For: 50.23.41.34, 3.54.85.90, 110.34.87.34, 10.43.21.25" -H "X-Forwarded-Port: 31173" -H "Origin: http://chall.ycfteam.in:6375/" -H "Age: 20" -H "Date: Mon, 27 May 2024 04:30:00 GMT"
```


# Stega

## Valour

given png image

![courage](https://github.com/user-attachments/assets/002fc497-1b3b-405d-a24f-35d5f86576d6)

```binwalk courage.png```

```binwalk --d=".*" courage.png```

```mv 30213 hidden.zip```

```zip2john hidden.zip pass.hash```

```john pass.hash --wordlist=/usr/share/wordlists/rockyou.txt```
