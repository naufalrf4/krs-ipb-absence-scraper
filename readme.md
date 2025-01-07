
---

# KRS IPB Absence Scraper
---
## **Description**
KRS IPB Absence Scraper  is an advanced automation tool for retrieving student attendance data from IPB University's course registration system.

---

## **Author**
- **Name**: Naufal Rizqullah F  
- **Contact**: [naufalrf4@gmail.com](mailto:naufalrf4@gmail.com)  

---

## **Requirements**
Before running the script, ensure you have the following installed:

1. **Python 3.9 or higher**: Download from [python.org](https://www.python.org/downloads/).
2. **Google Chrome**: Download from [google.com/chrome](https://www.google.com/chrome/).
3. **ChromeDriver**: Download the version matching your Chrome browser from [ChromeDriver](https://sites.google.com/chromium.org/driver/).
4. **Environment Variables**: Create a `.env` file to store your credentials and ChromeDriver path.

---

## **Download**
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/krs-ipb-absence-scraper.git
   cd krs-ipb-absence-scraper
   ```

---

## **Environment Settings**
1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open the `.env` file and update the following variables:
   ```env
   KRS_USERNAME=your_student_username
   KRS_PASSWORD=your_student_password
   CHROMEDRIVER_PATH=/path/to/chromedriver
   ```
   Replace `your_student_username`, `your_student_password`, and `/path/to/chromedriver` with your actual credentials and ChromeDriver path.

---

## **Install Requirements**
1. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Setup**
1. Ensure the `.env` file is correctly configured.
2. Verify that ChromeDriver is installed and the path is correct in the `.env` file.

---

## **Run the Script**
1. Activate the virtual environment (if not already activated):
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Run the script:
   ```bash
   python main.py
   ```

---

## **Tutorial: How to Use the Scraper**
1. **Login**: The script will automatically log in to the KRS IPB system using your credentials.
2. **Enter Course Code**: You will be prompted to enter the course code for which you want to retrieve attendance data.
3. **Select Class**: The script will display a list of available classes. Select the desired class by entering its number.
4. **Scrape Data**: The script will scrape student attendance data and save it to an Excel file.
5. **Output**: The Excel file will be saved in the project directory with the name `[course_code]_attendance.xlsx`.

---

## **Example Workflow**
1. Run the script:
   ```bash
   python main.py
   ```
2. The script will log in and prompt you to enter a course code:
   ```
   Masukkan kode mata kuliah: ABC123
   ```
3. The script will display available classes:
   ```
   Kelas yang tersedia:
   1. A1 - Senin 08:00-10:00
   2. A2 - Selasa 10:00-12:00
   ```
4. Select a class by entering its number:
   ```
   Pilih nomor kelas yang diinginkan: 1
   ```
5. The script will scrape the data and save it to `ABC123_attendance.xlsx`.

---

## **Troubleshooting**
- **WebDriver Issues**: Ensure the correct version of ChromeDriver is installed and matches your Chrome browser version.
- **Login Failures**: Double-check your `.env` file to ensure the username and password are correct.
- **Timeout Errors**: If the script times out, ensure your internet connection is stable and the KRS IPB system is accessible.

---

## **Changelog**
- **v1.0.0** (2024-12-05): Initial release with basic functionality for scraping attendance data.

---

## **Contact Information**
For questions or feedback, please contact:  
- Name: Naufal Rizqullah F  
- Email: [naufalrf4@gmail.com](mailto:naufalrf4@gmail.com)  
- GitHub: [naufalrf4](https://github.com/naufalrf4)  

---

### **Notes**
1. **Help with `requirements.txt`**: The `requirements.txt` file is already provided above. It includes the necessary Python packages for the project.
2. **Copy `.env.example`**: Use the `.env.example` file as a template to create your `.env` file and update it with your credentials.
3. **Additional Notes**:
   - Ensure your Chrome browser is up-to-date.
   - If you encounter issues with ChromeDriver, download the correct version for your Chrome browser.
