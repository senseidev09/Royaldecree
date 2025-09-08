# **auditwf**

## **What is Auditwf?**
Auditwf is an **Advanced tool that automates monitoring of the Windows Firewall log file to detect and record security events. Its main purpose is to notify the user about network activities, such as blocked or allowed connection attempts, and to record relevant information for further analysis.**

---

# **Features**
- **Monitor firewall events**
- **Collect detailed information**   
- **Send email alerts**
- **Create a permanent record** 
- **geolocation**  

---

# **Setup & Installation**
-**Install python 3 Install**
-**Install the necessary libraries by running in your terminal.**

```bash
pip install requests
```

---


##**Turn on Firewall Logging:**

Go to Windows Defender Firewall with Advanced Security. In Firewall Properties, in the Logging section, set "Log (dropped packets)" to Yes.


###**Edit the email configuration section with your information:**

-email_from: Your email address. 
-email_to: The destination email address. -app_password: The app password for your email account.

---

### **Navigate to the folder where you saved the file**
Run:
```bash
cd c:\monitoring
```

###**Run to script**
```bash
python auditwf.py
```

---

# **Author Information**
- **Author:**[josh lopez](https://github.com/senseidev09/senseidev09)  

