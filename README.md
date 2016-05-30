### FireTrail Project by 0pc0d3.

This project is designed to track vendor updates, look for specific update keywords and notify the user of matching vendor signature.

Currently, it only tracks SNORT and Emerging Threat updates.

This project has 3 components.

1. Update Checker - visits the update page and parses the vendor signature list and dumps it into a file.
2. Crawler - Checks the dump file for matching key words and dumps it into another file.
3. Notifyer - E-mails the end user for the new updates that match the keywords.


