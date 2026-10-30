import csv


class SupplierRiskExpertSystem:
    """A rule-based expert system that evaluates a supplier's overall risk profile

    based on geopolitical exposure, dependency, financial stability, and
    transit routes.
    """

    def evaluate_supplier(self, supplier):
        name = supplier["supplier_name"]
        country_risk = int(supplier["country_risk_score"])  # Scale 1 to 10
        is_single_source = supplier["single_source"].strip().upper() == "YES"
        financial_score = int(
            supplier["financial_health_score"]
        )  # Scale 1 (Poor) to 10 (Strong)
        transit_chokepoint = (
            supplier["chokepoint_exposure"].strip().upper() == "YES"
        )

        risk_score = 0
        flags = []
        recommendations = []

        # Rule 1: Geopolitical / Country Risk
        if country_risk >= 7:
            risk_score += 35
            flags.append(
                f"High Geopolitical Risk (Country Score: {country_risk}/10)"
            )
            recommendations.append(
                "Identify alternative suppliers in stable regions (Friendshoring)."
            )
        elif country_risk >= 4:
            risk_score += 15

        # Rule 2: Single Source Dependency
        if is_single_source:
            risk_score += 25
            flags.append("Single-Source Vulnerability (No Secondary Supplier)")
            recommendations.append(
                "Qualify a secondary backup supplier to prevent single-point failure."
            )

        # Rule 3: Financial Health
        if financial_score <= 3:
            risk_score += 25
            flags.append(
                f"Weak Financial Health (Score: {financial_score}/10)"
            )
            recommendations.append(
                "Conduct audit; request escrow or shorter payment terms."
            )
        elif financial_score <= 6:
            risk_score += 10

        # Rule 4: Logistics & Maritime Chokepoint Risk
        if transit_chokepoint:
            risk_score += 15
            flags.append("Transit Route Passes Contested Maritime Chokepoint")
            recommendations.append(
                "Evaluate overland or alternative maritime freight routes."
            )

        # Determine Final Risk Category
        if risk_score >= 70:
            category = "CRITICAL RISK"
        elif risk_score >= 40:
            category = "HIGH RISK"
        elif risk_score >= 20:
            category = "MEDIUM RISK"
        else:
            category = "LOW RISK"

        return {
            "supplier_name": name,
            "risk_score": risk_score,
            "category": category,
            "flags": flags,
            "recommendations": recommendations,
        }


def run_assessment():
    system = SupplierRiskExpertSystem()

    print("=" * 60)
    print("        SUPPLIER RISK PROFILE EVALUATION REPORT")
    print("=" * 60)

    try:
        with open("suppliers.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                result = system.evaluate_supplier(row)

                print(
                    f"\n[+] Supplier: {result['supplier_name']}"
                )
                print(
                    f"    Overall Risk Score: {result['risk_score']}/100  -->  [{result['category']}]"
                )

                if result["flags"]:
                    print("    Risk Flags:")
                    for flag in result["flags"]:
                        print(f"      - {flag}")

                    print("    Recommended Mitigation:")
                    for rec in result["recommendations"]:
                        print(f"      * {rec}")
                else:
                    print("    Status: Acceptable risk profile.")

                print("-" * 60)

    except FileNotFoundError:
        print(
            "Error: 'suppliers.csv' file not found. Ensure it is in the same folder."
        )


if __name__ == "__main__":
    run_assessment()