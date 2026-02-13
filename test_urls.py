import opengeo as og

# Get all known aliases and URLs
print(og.Aliases())
print(og.Urls())

# Initialize a specific catalog
og.Initialize('MICROSOFT')

# Get all collections available at Microsoft Planetary Computer
collections = og.Collections()
print(f"Available collections: {collections[:5]}") 
# Output: ['daymet-annual-pr', 'daymet-daily-hi', '3dep-seamless', ...]
