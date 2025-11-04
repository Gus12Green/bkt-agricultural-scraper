# BKT Agricultural Scraper

This project is a **Python web scraper** built with **Selenium** that automatically navigates through the official **BKT Tires (Spanish website)** and extracts detailed information about all agricultural tires listed in their public catalog.

The goal of this script is to collect structured data for analysis, research, and internal catalog organization.  
All the information gathered is **publicly available** on the official BKT website and is **used exclusively for educational and analytical purposes**.

---

## 🧰 Features

- Automated navigation through BKT’s agricultural tire catalog.
- Extraction of key product attributes:
  - **Model**
  - **Construction type**
  - **Compatible vehicles**
  - **Main applications / uses**
  - **Product URL**
- Data is saved locally in a **CSV file** for further use in data analysis or integration with BI tools.

---

## 🕹️ Technologies Used

- **Python 3.10+**
- **Selenium**
- **Pandas**
- **Chrome WebDriver (or Edge/Firefox compatible)**

---

## 📁 Output Example

The script generates a CSV file similar to the following:

| model         | construction | vehicles         | uses                      | url                                |
|----------------|---------------|------------------|----------------------------|------------------------------------|
| AGRIMAX FORCE  | Radial        | Tractors         | Field & transport          | https://www.bkt-tires.com/...      |
| RIDEMAX FL 693M| Bias          | Trailers         | Road & multipurpose        | https://www.bkt-tires.com/...      |

---

## 👨‍💻 Author

Created with care and curiosity by **Agustin Gorrin**.

---

## 📫 Contact

- GitHub: [https://github.com/gus12green](https://github.com/gus12green)
- LinkedIn: [https://linkedin.com/in/agustín-gorrín-santana/](https://linkedin.com/in/agustín-gorrín-santana/)

---

## ⚖️ Disclaimer

This scraper only collects **publicly available data** from the [official BKT website](https://www.bkt-tires.com/es/es) and **does not bypass any access restrictions**.  
The purpose of this project is **educational**, intended to demonstrate responsible data collection and automation techniques with Selenium.

If you are a representative of BKT and wish to have this repository removed or modified, please feel free to contact me, the repository owner.

---
