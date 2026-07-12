<h1 align="center">Cyberia</h1>

<p align="center">
Open-source imageboard focused on privacy.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![WTForms](https://img.shields.io/badge/WTForms-4B8BBE?style=for-the-badge)
![Jinja](https://img.shields.io/badge/Jinja-B41717?style=for-the-badge&logo=jinja&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![GPL-3.0](https://img.shields.io/badge/License-GPLv3-blue?style=for-the-badge&logo=gnu&logoColor=white)

</p>

---

## About

Cyberia is an open-source imageboard built with Flask. It is designed to be lightweight, self-hostable, and focused on privacy.

---

## Features

- User authentication
- Thread creation
- Replies
- Image uploads
- Administrative dashboard

---

## Tech Stack

- Python
- Flask
- SQLAlchemy
- WTForms
- Jinja2
- Pillow
- bcrypt
- SQLite

---

## Installation

Clone the repository.

```bash
git clone https://github.com/nullbyteSec1/Cyberia.git
cd Cyberia
```

Create a virtual environment (recommended).

```bash
python -m venv .venv
```

Linux/macOS

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Install the dependencies.

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a file named `config.json` in the project root.

```json
{
    "hosting": "localhost",
    "porting": 8080,
    "secret_key": "change_this_to_a_random_secret",
    "upload_folder": "./uploads"
}
```

### Configuration options

| Key | Description |
|------|-------------|
| `hosting` | Address where the server will listen. |
| `porting` | HTTP server port. |
| `secret_key` | Secret key used by Flask sessions. Use a long random value in production. |
| `upload_folder` | Directory where uploaded images are stored. |

---

## Running

Start the application.

```bash
python app.py
```

Open your browser.

```
http://localhost:8080
```

---

## Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Open a Pull Request.

---

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).

See the `LICENSE` file for details.
