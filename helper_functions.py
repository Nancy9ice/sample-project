import requests
from datetime import datetime
import pandas as pd
import uuid
import pandasql as ps
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def fetch_users(n=500, nationality="ca", seed="vendease"):
    """
    Fetches data from the Random User Generator API.

    Parameters:
    - n (int): The number of users to fetch (default is 500 as instructed).
    - nationality (str): The nationality of the users to fetch (default is "ca" for Canada).
    - seed (str): The seed value for the API request (default is "vendease" as instructed).

    Returns:
    - list: A list of dictionaries containing user details.

    Raises:
    - Exception: If the API request fails, an exception is raised.
    """

    url = f"https://randomuser.me/api/?page=1&results={n}&nat={nationality}&seed={seed}"
    
    logging.info(f"Fetching {n} users from API with nationality '{nationality}' and seed '{seed}'...")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for non-200 responses
        members = response.json()["results"]
        logging.info(f"Successfully fetched {len(members)} users.")
        return members
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch users: {e}")
        raise Exception("Failed to fetch users") from e
    

class Member:
    """
    Creates a Member Class with personal details, registration date, and address.

    Attributes:
    - uuid (str): Unique identifier for the member.
    - fullname (str): Full name of the member comprising of first and last name.
    - email (str): Email address of the member.
    - age (float): Age of the member.
    - gender (str): Gender of the member.
    - id (str): ID value assigned to the member.
    - registered_date (datetime): The date and time the member registered which is parsed into a datetime object.
    - address (str): The full address of the member containing "street, postcode and city".


    Returns:
        string: The member's details.
    """

    def __init__(self, uuid, first_name, last_name, email, age, gender, id_value, registered_date, street, postcode, city):
        self.uuid = uuid
        self.fullname = f"{first_name} {last_name}"
        self.email = email
        self.age = age
        self.gender = gender
        self.id = id_value
        self.registered_date = datetime.strptime(registered_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.address = f"{street}, {postcode} {city}"

    def __str__(self):
        return (f"UUID: {self.uuid}\n"
                f"Fullname: {self.fullname}\n"
                f"Email: {self.email}\n"
                f"Age: {self.age}\n"
                f"Gender: {self.gender}\n"
                f"ID: {self.id}\n"
                f"Registered Date: {self.registered_date}\n"
                f"Address: {self.address}")
    

def create_members(members):
    """
    Using the Member Class, the API query results are converted into a structured list of member dictionaries.

    Parameters:
    - members (list of dicts): containing user data dictionaries fetched from the API.

    Returns:
    - list of dicts: where each dictionary represents a member with their associated details.
    """

    logging.info("Starting member creation process...")

    member_data = []  

    for index, user_data in enumerate(members):
        try:
            # Create the Member object using the user data
            member = Member(
                uuid=user_data["login"]["uuid"],  
                first_name=user_data["name"]["first"],  
                last_name=user_data["name"]["last"],  
                email=user_data["email"],  
                age=user_data["dob"]["age"],  
                gender=user_data["gender"],  
                id_value=user_data["id"]["value"],  
                registered_date=user_data["registered"]["date"],  
                street=f"{user_data['location']['street']['number']} {user_data['location']['street']['name']}", 
                postcode=user_data["location"]["postcode"], 
                city=user_data["location"]["city"]  
            )

            # Append the processed member data as a dictionary to the defined list
            member_data.append({
                "UUID": member.uuid,  
                "Fullname": member.fullname,  
                "Email": member.email,  
                "Age": member.age,  
                "gender": member.gender,  
                "ID": member.id,  
                "registered_date": member.registered_date,  
                "Address": member.address  
            })

            if (index + 1) % 100 == 0:  # Log progress for every 100 members
                logging.info(f"Processed {index + 1} members...")

        except KeyError as e:
            logging.error(f"Missing key {e} in user data: {user_data}")
        except Exception as e:
            logging.error(f"Error processing user data: {e}")

    logging.info(f"Member creation completed. Total members processed: {len(member_data)}")
    
    return member_data


def filter_mentors_and_mentorees(member_data):
    """
    Filters the mentors and mentorees from the member_data processed from the Member Class

    Parameters:
    - member_data (list of dict): Contains the members processed using the Member Class

    Returns:
    - mentors: A list containing the mentors and their details
    - mentorees: A list containing the mentorees and their details
    """

    logging.info("Starting filtering process for mentors and mentorees...")

    # Define the empty lists for both mentors and mentorees
    mentors = []
    mentorees = []

    for index, user in enumerate(member_data):
        try:
            # Define the member's age
            age = user["Age"]

            # Mentor criteria: Female, at least 40 years old, joined on or before 2004-01-01
            if user["gender"] == "female" and age >= 40 and user["registered_date"] <= datetime(2004, 1, 1):
                mentors.append(user)

            # mentoree criteria: Any gender, 30 years old or younger
            if age <= 30:
                mentorees.append(user)

            # Log progress every 100 members processed
            if (index + 1) % 100 == 0:
                logging.info(f"Processed {index + 1} members...")

        except KeyError as e:
            logging.error(f"Missing key {e} in user data: {user}")
        except Exception as e:
            logging.error(f"Error processing user data: {e}")

    logging.info(f"Filtering completed: {len(mentors)} mentors, {len(mentorees)} mentorees identified.")
    
    return mentors, mentorees


class Mentorships:
    """
    Creates the Mentorship Class that will assign mentors to their registered mentorees

    Attributes:
    - uuid (str): Unique identifier for the member.
    - mentor_uuid (str): Unique identifier for the Mentor
    - mentoree_uuid (str): Unique identifier for the mentoree

    Returns:
        string: The mentors and mentorees mentorship mapping.
    """
    def __init__(self, uuid, mentor_uuid, mentoree_uuid):
        self.uuid = uuid
        self.mentor_uuid = mentor_uuid
        self.mentoree_uuid = mentoree_uuid

    def __str__(self):
        return (f"UUID: {self.uuid}\n"
                f"Mentor_uuid: {self.mentor_uuid}\n"
                f"Mentoree_uuid: {self.mentoree_uuid}\n"
                )


def create_mentorships(mentors, mentorees):
    """
    Using the Mentorship Class, this creates an object containing mentors and their assigned mentorees.

    Parameters:
    - mentors (list of dicts): containing mentors and their details.
    - mentorees (list of dicts): containing mentorees and their details.

    Returns:
    - list of dicts: where each dictionary the mapping of mentorees to mentors.
    """

    logging.info("Starting mentorship assignment process...")

    mentorship_data = []

    # find the number of mentors and mentorees
    num_mentors = len(mentors)
    num_mentorees = len(mentorees)

    if num_mentors == 0 or num_mentorees == 0:
        logging.warning("Mentorship process cannot proceed: Either no mentors or no mentorees available.")
        return []

    logging.info(f"Total mentors: {num_mentors}, Total mentorees: {num_mentorees}")

    for index, (mentor, mentoree) in enumerate(zip(mentors, mentorees)):
        try:
            # Create a Mentorship object
            mentorship = Mentorships(
                uuid=str(uuid.uuid4()),
                mentor_uuid=mentor["UUID"],
                mentoree_uuid=mentoree["UUID"]
            )

            # Append mentorship data to the list
            mentorship_data.append({
                "UUID": mentorship.uuid,
                "Mentor_uuid": mentorship.mentor_uuid,
                "Mentoree_uuid": mentorship.mentoree_uuid
            })

            # Log progress every 50 assignments
            if (index + 1) % 50 == 0:
                logging.info(f"Assigned {index + 1} mentorship pairs...")

        except KeyError as e:
            logging.error(f"Missing key {e} in mentor or mentoree data: {mentor} | {mentoree}")
        except Exception as e:
            logging.error(f"Error creating mentorship: {e}")

    logging.info(f"Mentorship assignment completed: {len(mentorship_data)} pairs created.")
    
    return mentorship_data


def assign_mentorships(mentors, mentorees):
    """
    Assign mentorees to the Mentors using the Round-Robin Allocation Method.

    Parameters:
    - mentors (list of dicts): containing mentors and their details.
    - mentorees (list of dicts): containing mentorees and their details.

    Returns:
    - list of dicts: where each dictionary the mapping of mentorees to mentors.
    """

    logging.info("Starting mentorship assignment process using Round-Robin allocation...")

    # Checks if there are mentors and mentorees available
    if not mentors:
        logging.warning("No mentors available for assignment.")
        return []
    if not mentorees:
        logging.warning("No mentorees available for assignment.")
        return []

    # Sort mentors and mentorees by their registered date
    mentors.sort(key=lambda m: m["registered_date"])
    mentorees.sort(key=lambda m: m["registered_date"])

    mentorships = []
    mentor_count = len(mentors)

    logging.info(f"Total mentors: {mentor_count}, Total mentorees: {len(mentorees)}")

    for index, mentoree in enumerate(mentorees):
        try:
            assigned_mentor = mentors[index % mentor_count]  # Round-robin allocation
            
            # Log each assignment
            logging.info(f"Assigning {mentoree['Fullname']} to mentor {assigned_mentor['Fullname']}.")

            # Call create_mentorships function to generate the mentorship relationship
            mentorship = create_mentorships([assigned_mentor], [mentoree]) # pass them as list to aid processing
            
            # Extend mentorships list with the newly created pairs
            mentorships.extend(mentorship)

            # Log progress every 50 assignments
            if (index + 1) % 50 == 0:
                logging.info(f"{index + 1} mentorees assigned...")

        except KeyError as e:
            logging.error(f"Missing key {e} in mentor or mentoree data: {assigned_mentor} | {mentoree}")
        except Exception as e:
            logging.error(f"Error during mentorship assignment: {e}")

    logging.info(f"Mentorship assignment completed: {len(mentorships)} pairs created.")

    return mentorships


def normalize_data(member_data, mentorships):
    """
    This turns the list of dictionaries to pandas dataframe

    Parameters:
    - member_data (list of dicts): Contains the objects generated by the Member Class from the API results.
    - mentorships (list of dicts): Contains the objects generated by the Mentorships Class from the mentor-mentoree mapping results.

    Returns:
    - member_df: Pandas dataframe containing the members data
    - mentorship_df: Pandas dataframe containing the mentorship data
    """

    logging.info("Starting the data normalization process...")

    # Check if there is any member data or mentorship data
    if not member_data:
        logging.warning("No member data available for normalization.")
    if not mentorships:
        logging.warning("No mentorship data available for normalization.")

    # Normalize the members data from json to dataframe
    logging.info("Normalizing member data...")
    member_df = pd.json_normalize(member_data)
    logging.info(f"Member data normalized. Shape of member dataframe: {member_df.shape}")

    # Normalize the mentorship data from json to dataframe
    logging.info("Normalizing mentorship data...")
    mentorship_df = pd.json_normalize(mentorships)
    logging.info(f"Mentorship data normalized. Shape of mentorship dataframe: {mentorship_df.shape}")

    logging.info("Data normalization completed.")

    return member_df, mentorship_df


def median_age_of_male_mentorees(member_df, mentorship_df):
    """
    This returns the Median age of mentorees that registered on or after 2010-01-01).

    Parameters:
    - member_df: Pandas dataframe containing the members data
    - mentorship_df: Pandas dataframe containing the mentorship data

    Returns:
    - median_age: Median age of the male mentorees
    """

    logging.info("Starting the process to calculate the median age of male mentorees...")

    # Merge the dataframes to get the relevant data for mentorees
    logging.info("Merging the member and mentorship dataframes...")
    mentorees_df = pd.merge(member_df, mentorship_df, left_on='UUID', right_on='Mentoree_uuid', how='inner')
    logging.info(f"Merged dataframe shape: {mentorees_df.shape}")

    # Filter for male mentorees who registered after 2010-01-01
    logging.info("Filtering male mentorees who registered on or after 2010-01-01...")
    filtered_mentorees = mentorees_df[(mentorees_df['gender'] == 'male') & (mentorees_df['registered_date'] >= '2010-01-01')]

    # Log if no mentorees match the criteria
    if filtered_mentorees.empty:
        logging.warning("No male mentorees found who registered after 2010-01-01.")
    else:
        logging.info(f"Found {len(filtered_mentorees)} male mentorees who registered after 2010-01-01.")

    # Calculate the median age
    logging.info("Calculating the median age of filtered male mentorees...")
    median_age = filtered_mentorees['Age'].median()

    # Log the result
    logging.info(f"The median age of male mentorees is: {median_age}")

    return median_age


def total_mentorees_by_gender_and_mentor_age(mentorship_df, member_df):
    """
    Count mentorees by gender who are mentored by mentors that are at least 60 years old.

    Parameters:
    - member_df: Pandas dataframe containing the members data
    - mentorship_df: Pandas dataframe containing the mentorship data

    Returns:
    - result: Pandas dataframe that summarizes count of the mentorees (with 60 years or older mentors) by their gender
    """

    logging.info("Starting the process to count mentorees by gender and mentor age...")

    # SQL query to count mentorees by gender who are mentored by mentors at least 60 years old.
    query = """
    SELECT gender, COUNT(DISTINCT Mentoree_uuid) AS gender_count
    FROM mentorship_df
    JOIN member_df ON mentorship_df.Mentoree_uuid = member_df.UUID
    WHERE mentor_uuid IN (
    SELECT DISTINCT mentor_uuid
    FROM mentorship_df
    JOIN member_df ON mentorship_df.mentor_uuid = member_df.UUID
    WHERE member_df.Age >= 60)
    GROUP BY gender;
    """

    logging.info("Executing SQL query to count mentorees by gender for mentors at least 60 years old...")

    # Execute the query on the merged DataFrame
    result = ps.sqldf(query, locals())

    logging.info("Query executed successfully.")

    # Log the result
    logging.info(f"Result summary:\n{result.head()}")

    return result


def check_discrepancies(member_df, mentorship_df):
    """
    Checks for results that don't match the criteria of mentors and mentorees in the members dataframe

    Parameters:
    - member_df: Pandas dataframe containing the members data
    - mentorship_df: Pandas dataframe containing the mentorship data

    Returns:
    - invalid_mentors: Mentors that don't match the criteria of members (females, younger than 40 years, and registered_date before or on 2004-01-01) in the members dataframe.
    - invalid_mentors: Mentorees that don't match the criteria of members (is or is younger than 30 years) in the members dataframe.
    """

    logging.info("Starting the discrepancy check process...")

    # Merge mentorship_df with member_df to get mentor and mentoree details
    logging.info("Merging mentorship_df with member_df to get mentor and mentoree details...")
    mentorship_merged = mentorship_df \
        .merge(member_df[['UUID', 'gender', 'Age', 'registered_date']], left_on='Mentor_uuid', right_on='UUID', how='left') \
        .rename(columns={'gender': 'Mentor_gender', 'Age': 'Mentor_Age', 'registered_date': 'Mentor_registered_date'}) \
        .merge(member_df[['UUID', 'gender', 'Age']], left_on='Mentoree_uuid', right_on='UUID', how='left') \
        .rename(columns={'gender': 'Mentoree_gender', 'Age': 'Mentoree_Age'})

    logging.info("Merging completed successfully.")

    # Find invalid mentors
    logging.info("Identifying invalid mentors...")
    invalid_mentors = mentorship_merged[
        ~((mentorship_merged['Mentor_gender'] == 'female') &
          (mentorship_merged['Mentor_Age'] >= 40) &
          (mentorship_merged['Mentor_registered_date'] <= pd.Timestamp("2004-01-01")))
    ]
    logging.info(f"Found {len(invalid_mentors)} invalid mentors.")

    # Find invalid mentorees
    logging.info("Identifying invalid mentorees...")
    invalid_mentorees = mentorship_merged[
        ~(mentorship_merged['Mentoree_Age'] <= 30)
    ]
    logging.info(f"Found {len(invalid_mentorees)} invalid mentorees.")

    return invalid_mentors, invalid_mentorees