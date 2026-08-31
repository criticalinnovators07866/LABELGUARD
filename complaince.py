import re


def check_compliance(text):

    text_lower = text.lower()

    results = {}

    # 1. MRP
    results["MRP"] = bool(
        re.search(
            r"(mrp|maximum retail price).{0,30}(\₹|rs\.?|inr)?\s*\d+",
            text_lower
        )
    )

    # 2. Net Quantity
    results["Net Quantity"] = bool(
        re.search(
            r"(net\s*(quantity|qty|wt|weight)|net content).{0,30}\d+",
            text_lower
        )
    )

    # 3. Manufacturer
    results["Manufacturer"] = any(
        phrase in text_lower
        for phrase in [
            "manufactured by",
            "manufacturer",
            "manufactured & packed by",
            "manufactured and packed by",
            "packed by"
        ]
    )

    # 4. Manufacturer Address
    results["Manufacturer Address"] = bool(
        re.search(
            r"(address|road|street|nagar|industrial area|pincode|pin code)",
            text_lower
        )
    )

    # 5. Consumer Care
    results["Consumer Care"] = any(
        phrase in text_lower
        for phrase in [
            "customer care",
            "consumer care",
            "care number",
            "helpline",
            "toll free",
            "contact us"
        ]
    )

    # 6. Country of Origin
    results["Country of Origin"] = any(
        phrase in text_lower
        for phrase in [
            "country of origin",
            "made in india",
            "made in"
        ]
    )

    # 7. Manufacturing / Packing Date
    results["Manufacturing / Packing Date"] = any(
        phrase in text_lower
        for phrase in [
            "manufactured on",
            "manufactured date",
            "mfg date",
            "mfg.",
            "packed on",
            "packing date",
            "date of packing"
        ]
    )

    # 8. Best Before / Use By
    results["Best Before / Use By"] = any(
        phrase in text_lower
        for phrase in [
            "best before",
            "best before end",
            "use by",
            "expiry",
            "expires"
        ]
    )

    # 9. Product / Generic Name
    results["Product Name"] = len(text.strip()) > 5

    # 10. Unit Sale Price
    results["Unit Sale Price"] = any(
        phrase in text_lower
        for phrase in [
            "unit sale price",
            "price per",
            "₹/kg",
            "₹/g",
            "rs/kg",
            "rs/g"
        ]
    )

    # Calculate score
    passed = sum(results.values())
    total = len(results)

    score = round((passed / total) * 100)

    return results, score