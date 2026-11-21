# ACCESScheck

AccessCheck is a local Flask demo showing role and MFA-based access decisions.<br/>
It helps to illustrate why an IP address or VPN location should not be the sole basis for granting access.

## Features

- Choose from fictional demo users
- Check access based on role and MFA status
- Try a simulated sensitive action
- View recent allowed and denied actions in an audit log

## Demo users

| User | Role | MFA | Sensitive action |
|---|---|---|---|
| Alex Demo | Viewer | Enabled | Denied — admin role required |
| Sam Demo | Admin | Disabled | Denied — MFA required |
| Jordan Demo | Admin | Enabled | Allowed |

## Run locally

You’ll need Python 3.10 or newer.

## 1. Clone the repository and open its folder:

   ```bash
   git clone https://github.com/YOUR-USERNAME/accesscheck.git
   cd accesscheck
   ```

## 2. Create and activate a virtual environment:

  ```bash
    python -m venv .venv
  ```

- **For macOS/Linux:**

  ```bash
     source .venv/bin/activate
  ```

- **For Windows PowerShell:**

  ```bash
    .venv\Scripts\Activate.ps1
  ```

## 3. Install the dependencies:
   
  ```bash
    pip install -r requirements.txt
  ```

## 4. Set a local secret key.

- For macOS/Linux:
  
  ```bash
  export SECRET\_KEY="replace-this-with-a-random-value"
  ```

- For Windows PowerShell:
  
  ```bash
  \$env:SECRET\_KEY="replace-this-with-a-random-value"
  ```

## 5. Start the app:

  ```bash
  python app.py
  ```

## 6. Open http://127.0.0.1:5000 in your browser.

# How the demo works

The app grants the simulated sensitive action only when the user has both the admin role and MFA enabled.<br/> 
Its access policy does not use IP address or VPN location.

## Project Structure
accesscheck/ <br/>
├── app.py <br/>
├── requirements.txt <br/>
├── README.md <br/>
└── templates/ <br/>
____├── index.html <br/>
____└── dashboard.html

## Scope and limitations
<strong><ins>This is an educational local demo, not production authentication software.</ins></strong> <br/> 
It uses fictional users and does not verify passwords or implement real MFA.<br/> 
Do not use it to protect real data or deploy it publicly.<br/> 
Flask’s built-in development server is for local development only.

## MIT License. 
See the [LICENSE](LICENSE) file for details.
