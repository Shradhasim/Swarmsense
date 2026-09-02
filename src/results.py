import csv


def save_results(results, filename):
    
    # Saves simulation results to a CSV file.
    
    if not results:
        return

    fieldnames = results[0].keys()

    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(results)