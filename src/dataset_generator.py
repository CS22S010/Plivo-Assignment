import json
import random
import re

NUM_TRAIN = 500
NUM_DEV = 150

OUTPUT_TRAIN_FILE = "generated_train.jsonl"
OUTPUT_DEV_FILE = "generated_dev.jsonl"

random.seed(42)

DIGIT_WORD = {
    "0": "zero",
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine",
}

def number_to_spelled_digits(num_str, group=False):
    """
    Convert '1234' -> 'one two three four'
    If group=True, insert grouping hints like 'double' etc. occasionally.
    """
    words = [DIGIT_WORD[d] for d in num_str]
    if not group:
        return " ".join(words)
    # very simple grouping noise: sometimes join two digits with "double"
    i = 0
    out = []
    while i < len(words):
        if i + 1 < len(words) and random.random() < 0.2:
            # pretend the next digit repeats ("double three") even if it doesn't, just noise
            out.append("double " + words[i])
            i += 2
        else:
            out.append(words[i])
            i += 1
    return " ".join(out)


def build_credit_cards(n=60):
    # base 16-digit card numbers (fake)
    base_cards = [
        "4299001287563210",
        "5111600073442111",
        "3792801799949635",
        "4248556420182411",
        "4012888891910022",
        "5555555555554444",
        "4111111111111111",
        "4000001234567899",
        "6011000990139424",
        "3530111333300000",
        "5105105105105100",
        "4007000000027",
        "2223000048400011",
        "5200828282828210",
        "5100000000000008",
        "4485275742308327",
        "4716108999716531",
        "6011911111111113",
        "6011000400000000",
        "378282246310005",
        "371449635398431",
        "30569309025904",
        "38520000023237",
        "3566002020360505",
    ]
    # create extra cards by randomizing
    while len(base_cards) < n:
        num = "".join(str(random.randint(0, 9)) for _ in range(random.choice([15, 16])))
        base_cards.append(num)

    examples = []
    for card in base_cards:
        # two variants per card
        examples.append(number_to_spelled_digits(card, group=False))
        examples.append(number_to_spelled_digits(card, group=True))
    # ensure at least n
    return examples[:max(n, 50)]

def build_phones(n=60):
    base_phones = [
        "9876543210",
        "1234567890",
        "9001882627",
        "9783192211",
        "9988776655",
        "9123456789",
        "7001234567",
        "8080808080",
        "9990001112",
        "8887776665",
        "919876543210",
        "918888777766",
        "919900112233",
    ]
    while len(base_phones) < n:
        length = random.choice([10, 11, 12])
        num = "".join(str(random.randint(0, 9)) for _ in range(length))
        base_phones.append(num)

    examples = []
    for ph in base_phones:
        spelled = number_to_spelled_digits(ph)
        examples.append(spelled)
        examples.append("plus nine one " + spelled if not ph.startswith("91") else spelled)
    return examples[:max(n, 50)]

def build_emails(n=60):
    firsts = [
        "john", "sneha", "michael", "lee", "anita", "rahul", "emily", "sanjay",
        "diana", "peter", "priya", "rohan", "nina", "arjun", "fatima", "luis",
        "kevin", "sara", "tom", "amrita"
    ]
    lasts = [
        "doe", "kumar", "ross", "wong", "verma", "sharma", "clark", "menon",
        "prince", "parker", "singh", "patel", "gupta", "iyer", "ali", "garcia",
        "brown", "lee", "roy", "nair"
    ]
    separators = [" dot ", " underscore ", ""]
    domains = [
        "gmail dot com", "yahoo dot com", "outlook dot com", "mail dot net",
        "example dot org", "service desk dot io", "customer support dot com",
        "protonmail dot com", "live dot com", "company dot co dot in"
    ]
    extras = ["info", "contact", "support", "help", "billing", "care", "team"]

    examples = []
    # generate many combos
    while len(examples) < n:
        if random.random() < 0.3:
            user = random.choice(extras)
        else:
            user = random.choice(firsts)
            if random.random() < 0.7:
                sep = random.choice(separators)
                user = user + sep + random.choice(lasts)
        email = user + " at " + random.choice(domains)
        examples.append(email)

    return examples[:max(n, 50)]

def build_person_names(n=60):
    firsts = [
        "john", "sneha", "michael", "lee", "anita", "rahul", "emily", "sanjay",
        "diana", "peter", "priya", "rohan", "nina", "arjun", "fatima", "luis",
        "kevin", "sara", "tom", "amrita", "yuki", "maria", "omar", "helen",
        "akash", "vidya", "ishaan", "noah", "ava", "liam", "olivia", "ethan"
    ]
    lasts = [
        "doe", "kumar", "ross", "wong", "verma", "sharma", "clark", "menon",
        "prince", "parker", "singh", "patel", "gupta", "iyer", "ali", "garcia",
        "brown", "lee", "roy", "nair", "fernandez", "silva", "nguyen", "kim",
        "mukherjee", "das", "reddy", "joshi", "khanna", "bose"
    ]
    examples = []
    while len(examples) < n:
        name = random.choice(firsts) + " " + random.choice(lasts)
        examples.append(name)
    return examples[:max(n, 50)]

def build_dates(n=60):
    day_words = [
        "first", "second", "third", "fourth", "fifth", "sixth", "seventh",
        "eighth", "ninth", "tenth", "eleventh", "twelfth", "thirteenth",
        "fourteenth", "fifteenth", "sixteenth", "seventeenth", "eighteenth",
        "nineteenth", "twentieth", "twenty first", "twenty second",
        "twenty third", "twenty fourth", "twenty fifth", "twenty sixth",
        "twenty seventh", "twenty eighth", "twenty ninth", "thirtieth",
        "thirty first"
    ]
    months = [
        "january", "february", "march", "april", "may", "june",
        "july", "august", "september", "october", "november", "december"
    ]
    years_words = [
        "two thousand eighteen", "two thousand nineteen",
        "two thousand twenty", "two thousand twenty one",
        "two thousand twenty two", "two thousand twenty three",
        "two thousand twenty four", "two thousand ten",
        "two thousand eleven", "two thousand twelve",
    ]
    examples = []

    # spelled-out date
    while len(examples) < n // 2:
        day = random.choice(day_words)
        month = random.choice(months)
        year = random.choice(years_words)
        examples.append(day + " " + month + " " + year)

    # numeric-ish with slashes
    while len(examples) < n:
        dd = str(random.randint(1, 28)).zfill(2)
        mm = str(random.randint(1, 12)).zfill(2)
        yy = random.choice(["twenty twenty", "twenty twenty one", "twenty twenty two"])
        examples.append(f"{dd} slash {mm} slash {yy}")
    return examples[:max(n, 50)]

def build_cities(n=60):
    cities = [
        "san francisco", "new york", "mumbai", "bangalore", "delhi",
        "tokyo", "london", "hyderabad", "toronto", "dubai",
        "chennai", "pune", "kolkata", "los angeles", "chicago",
        "paris", "berlin", "sydney", "melbourne", "singapore",
        "hong kong", "seoul", "amsterdam", "zurich", "vienna",
        "rome", "madrid", "lisbon", "vancouver", "montreal",
        "bengaluru", "ahmedabad", "jaipur", "lucknow", "kochi",
        "doha", "abu dhabi", "shanghai", "beijing", "shenzhen",
        "san jose", "phoenix", "houston", "miami", "boston",
        "seattle", "san diego", "brisbane", "auckland", "osaka",
        "nagoya", "helsinki", "stockholm", "copenhagen", "oslo",
    ]
    random.shuffle(cities)
    return cities[:max(n, 50)]

def build_locations(n=60):
    streets = [
        "main street", "high street", "elm street", "oak street",
        "maple avenue", "pine avenue", "park road", "station road",
        "market road", "river road", "lake view road", "hill top road",
        "airport road", "ring road", "central avenue", "queen street",
        "king street", "fifth avenue", "broadway", "church street",
    ]
    area_mods = [
        "near city center", "near metro station", "near bus stop",
        "opposite mall", "behind hospital", "beside school",
        "near railway station", "close to river", "near old fort",
        "near tech park", "inside old town", "near market circle",
        "near central park", "near university gate",
    ]
    cities = build_cities(30)
    examples = []

    while len(examples) < n:
        street = random.choice(streets)
        mod = random.choice(area_mods)
        if random.random() < 0.5:
            loc = street + " " + mod
        else:
            loc = street + " " + random.choice(cities)
        examples.append(loc)
    return examples[:max(n, 50)]

# build final entity bank
ENTITY_VALUES = {
    "CREDIT_CARD": build_credit_cards(),
    "PHONE": build_phones(),
    "EMAIL": build_emails(),
    "PERSON_NAME": build_person_names(),
    "DATE": build_dates(),
    "CITY": build_cities(),
    "LOCATION": build_locations(),
}


SIMPLE_TEMPLATES = [
    # single-entity, minimal context
    "my email is {EMAIL}",
    "email id {EMAIL}",
    "send mail to {EMAIL}",
    "contact email {EMAIL}",
    "please use {EMAIL}",
    "my phone number is {PHONE}",
    "contact number {PHONE}",
    "reach me on {PHONE}",
    "you can call me at {PHONE}",
    "whatsapp number {PHONE}",
    "my card number is {CREDIT_CARD}",
    "credit card {CREDIT_CARD}",
    "debit card {CREDIT_CARD}",
    "card on file {CREDIT_CARD}",
    "my name is {PERSON_NAME}",
    "this is {PERSON_NAME}",
    "account holder {PERSON_NAME}",
    "city {CITY}",
    "i live in {CITY}",
    "currently in {CITY}",
    "i stay in {LOCATION}",
    "address {LOCATION}",
    "current address {LOCATION}",
    "permanent address {LOCATION}",
    "date is {DATE}",
    "booking date {DATE}",
    "delivery on {DATE}",
    "meeting on {DATE}",
    "nearest city {CITY}",
    "office at {LOCATION}",
    "head office in {CITY}",
    "send package to {LOCATION}",
    "ship to {LOCATION}",
    "traveling from {CITY}",
    "traveling to {CITY}",
    "destination city {CITY}",
    "pickup location {LOCATION}",
    "drop location {LOCATION}",
]

MEDIUM_TEMPLATES = [
    # 2 entities, short sentence
    "my name is {PERSON_NAME} and my email is {EMAIL}",
    "you can call me on {PHONE} and email {EMAIL}",
    "card {CREDIT_CARD} belongs to {PERSON_NAME}",
    "billing card {CREDIT_CARD} for {PERSON_NAME}",
    "update phone to {PHONE} for {PERSON_NAME}",
    "i moved to {CITY} on {DATE}",
    "i am staying at {LOCATION} in {CITY}",
    "ship the order on {DATE} to {LOCATION}",
    "deliver by {DATE} to {LOCATION}",
    "schedule appointment on {DATE} in {CITY}",
    "meeting in {CITY} on {DATE}",
    "traveling from {CITY} to {CITY} on {DATE}",
    "please contact {PERSON_NAME} on {PHONE}",
    "register {PERSON_NAME} with email {EMAIL}",
    "add new card {CREDIT_CARD} for account of {PERSON_NAME}",
    "use email {EMAIL} for all updates",
    "my work email is {EMAIL} and personal is {EMAIL}",
    "primary number {PHONE} and alternate {PHONE}",
    "my residence is {LOCATION} and city is {CITY}",
    "mark booking under {PERSON_NAME} in {CITY}",
    "emergency contact {PHONE} for {PERSON_NAME}",
    "conference is in {CITY} on {DATE}",
    "delivery city is {CITY} and address {LOCATION}",
    "the policy starts on {DATE} and holder is {PERSON_NAME}",
    "rent agreement location {LOCATION} signed on {DATE}",
    "use {EMAIL} and not the old one",
    "update city from {CITY} to {CITY}",
    "my address changed from {LOCATION} to {LOCATION}",
    "my phone changed from {PHONE} to {PHONE}",
    "trip booked from {CITY} to {CITY} on {DATE}",
    "please verify card {CREDIT_CARD} and phone {PHONE}",
    "ticket should show name {PERSON_NAME} and city {CITY}",
    "hotel booking under {PERSON_NAME} in {CITY}",
    "office branch is in {CITY} at {LOCATION}",
    "i was born on {DATE} in {CITY}",
    "appointment for {PERSON_NAME} at {LOCATION}",
    "save my contact {PHONE} as {PERSON_NAME}",
    "invoice address {LOCATION} in {CITY}",
    "main office at {LOCATION} and support email {EMAIL}",
]

COMPLEX_TEMPLATES = [
    # more natural, multi-entity, call-center-ish
    "okay so my name is {PERSON_NAME} and i need you to update my phone to {PHONE} and email to {EMAIL}",
    "please write this down my card number is {CREDIT_CARD} and it is linked to {PERSON_NAME} living in {CITY}",
    "for this booking use the name {PERSON_NAME} i will arrive in {CITY} on {DATE} and you can contact me at {PHONE}",
    "uh listen carefully my current address is {LOCATION} in {CITY} and my email on record should be {EMAIL}",
    "dont add punctuation just store this my phone is {PHONE} and my backup number is {PHONE} and the city is {CITY}",
    "for insurance details the policy holder is {PERSON_NAME} date of birth {DATE} and i live in {LOCATION} {CITY}",
    "can you change the shipping city to {CITY} and the address to {LOCATION} and confirm it to {EMAIL}",
    "i want to register {PERSON_NAME} with phone {PHONE} staying at {LOCATION} in {CITY} from {DATE}",
    "okay for my salary account the card is {CREDIT_CARD} and all statements should go to {EMAIL}",
    "please update both phone and email the new number is {PHONE} and the email is {EMAIL} for {PERSON_NAME}",
    "for the conference ticket use name {PERSON_NAME} the event is on {DATE} and venue is {LOCATION} in {CITY}",
    "this is important booking date is {DATE} travel from {CITY} to {CITY} and you must call me on {PHONE}",
    "write this exactly send the report on {DATE} to {EMAIL} and mention client name {PERSON_NAME} from {CITY}",
    "my office is in {CITY} at {LOCATION} but my home address is {LOCATION} and preferred email is {EMAIL}",
    "when you generate the invoice show customer as {PERSON_NAME} with contact {PHONE} and city {CITY}",
    "the package should reach {PERSON_NAME} at {LOCATION} in {CITY} before {DATE} and notify on {EMAIL}",
    "update your records i moved from {LOCATION} in {CITY} and now i stay at {LOCATION} in {CITY}",
    "if there is any issue call {PERSON_NAME} on {PHONE} or send an email to {EMAIL}",
    "for kyc details date of birth {DATE} full name {PERSON_NAME} city {CITY} and current address {LOCATION}",
    "uh i think your system still has my old city as {CITY} change it to {CITY} and keep phone {PHONE}",
    "for this order my billing address is {LOCATION} in {CITY} but shipping address is {LOCATION} in {CITY}",
    "alright so travel on {DATE} from {CITY} to {CITY} and keep my contact {PHONE} and email {EMAIL}",
    "when you send otp make sure it goes to {PHONE} and not to the old number also copy email to {EMAIL}",
    "the registered user is {PERSON_NAME} with credit card {CREDIT_CARD} and home city {CITY}",
    "i want customer profile for {PERSON_NAME} showing phone {PHONE} email {EMAIL} and city {CITY}",
    "please cancel previous booking on {DATE} from {CITY} and create a new one from {CITY} on {DATE}",
    "okay just confirming appointment for {PERSON_NAME} on {DATE} at {LOCATION} in {CITY}",
    "my official contact details are phone {PHONE} work email {EMAIL} and office location {LOCATION} {CITY}",
    "for emergency contact list add {PERSON_NAME} with number {PHONE} and address {LOCATION} in {CITY}",
    "the new tenant {PERSON_NAME} will move into {LOCATION} in {CITY} on {DATE} please note the phone {PHONE}",
    "for this credit card application my card number is {CREDIT_CARD} and current address is {LOCATION} {CITY}",
    "when you create the user id link it with email {EMAIL} phone {PHONE} and name {PERSON_NAME}",
    "all notifications about delivery on {DATE} to {LOCATION} in {CITY} should go to {EMAIL}",
    "the immigration form needs city of birth {CITY} date of birth {DATE} and full name {PERSON_NAME}",
    "support team can reach me at phone {PHONE} during the day and email {EMAIL} after office hours",
    "booking name is {PERSON_NAME} staying at {LOCATION} in {CITY} arriving on {DATE} please confirm via {EMAIL}",
    "for bank records set my residential city as {CITY} correspondence address as {LOCATION} and contact {PHONE}",
    "this subscription is for {PERSON_NAME} and the renewal date is {DATE} invoice should go to {EMAIL}",
]

# combine all templates
TEMPLATES = SIMPLE_TEMPLATES + MEDIUM_TEMPLATES + COMPLEX_TEMPLATES


def inject_sentence_noise(text: str) -> str:
    """
    Apply light ASR-style noise occasionally: fillers, small mishears.
    """
    # fillers
    if random.random() < 0.2:
        text = "uh " + text
    if random.random() < 0.1:
        text = "okay " + text

    # mishear-like replacements
    replacements = [
        (" dot ", " daht "),
        (" at ", " aet "),
        (" zero ", " oh "),
        ("gmail", "gee mail"),
        ("underscore", "under score"),
    ]
    for old, new in replacements:
        if random.random() < 0.2:
            text = text.replace(old, " " + new + " ")

    # collapse double spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


PLACEHOLDER_PATTERN = re.compile(r"\{([A-Z_]+)\}")

def fill_template(template: str):
    """
    Given a template with placeholders like {EMAIL}, {PHONE},
    return (text, entities_list) where entities_list has (start, end, label).
    """
    text = template
    entities = []

    # Find placeholders in order
    matches = list(PLACEHOLDER_PATTERN.finditer(template))
    # we'll build the text gradually
    offset = 0
    result_parts = []
    last_idx = 0

    for m in matches:
        label = m.group(1)
        start_tmpl, end_tmpl = m.span()
        # add static part
        static_chunk = template[last_idx:start_tmpl]
        result_parts.append(static_chunk)
        offset += len(static_chunk)

        # pick a random value for this label
        value = random.choice(ENTITY_VALUES[label])
        value_text = value

        # entity span in final text
        ent_start = offset
        ent_end = ent_start + len(value_text)
        entities.append({"start": ent_start, "end": ent_end, "label": label})

        result_parts.append(value_text)
        offset = ent_end
        last_idx = end_tmpl

    # add remaining static tail
    result_parts.append(template[last_idx:])
    text = "".join(result_parts)
    text = re.sub(r"\s+", " ", text).strip()

    # adjust entity offsets if we apply noise later
    noisy_text = inject_sentence_noise(text)

    if noisy_text != text:
        # need to recompute offsets based on actual substrings
        updated_entities = []
        for ent in entities:
            span_text = text[ent["start"]:ent["end"]]
            # find first occurrence of that span in noisy_text
            new_start = noisy_text.find(span_text)
            if new_start == -1:
                # fallback: skip if cannot find (rare with mild noise)
                continue
            new_end = new_start + len(span_text)
            updated_entities.append({
                "start": new_start,
                "end": new_end,
                "label": ent["label"]
            })
        entities = updated_entities
    text = noisy_text

    return text, entities


def make_record(idx: int):
    template = random.choice(TEMPLATES)
    text, entities = fill_template(template)
    return {
        "id": f"utt_{idx:04d}",
        "text": text,
        "entities": entities
    }

def write_dataset(path: str, count: int):
    with open(path, "w", encoding="utf-8") as f:
        for i in range(count):
            rec = make_record(i)
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"wrote {count} examples to {path}")


if __name__ == "__main__":
    write_dataset(OUTPUT_TRAIN_FILE, NUM_TRAIN)
    write_dataset(OUTPUT_DEV_FILE, NUM_DEV)
    print("done.")
