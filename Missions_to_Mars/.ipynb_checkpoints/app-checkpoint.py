{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1a73ff60",
   "metadata": {},
   "outputs": [],
   "source": [
    "from flask import Flask, render_template, redirect\n",
    "from flask_pymongo import PyMongo\n",
    "import scrape_mars\n",
    "\n",
    "app = Flask(__name__)\n",
    "\n",
    "# Use flask_pymongo to set up mongo connection\n",
    "app.config[\"MONGO_URI\"] = \"mongodb://localhost:27017/mission_to_mars_app\"\n",
    "mongo = PyMongo(app)\n",
    "\n",
    "# Create main page\n",
    "@app.route(\"/\")\n",
    "def index():\n",
    "    mars_data = mongo.db.mars_data.find_one()\n",
    "    return render_template(\"index.html\", data = mars_data)\n",
    "\n",
    "# Create scrape page\n",
    "@app.route(\"/scrape\")\n",
    "def scraper():\n",
    "    mars_data = mongo.db.mars_data\n",
    "    mars_item_data = scrape_mars.scrape()\n",
    "    mars_data.update({}, mars_item_data, upsert=True)\n",
    "    return redirect(\"/\", code=302)\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    app.run(debug=True)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
