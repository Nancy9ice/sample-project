import logging
from helper_functions import (fetch_users, 
                              create_members, 
                              filter_mentors_and_mentorees, 
                              assign_mentorships, 
                              normalize_data, 
                              median_age_of_male_mentorees, 
                              total_mentorees_by_gender_and_mentor_age, 
                              check_discrepancies)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    try:
        # Step 1: Fetch Users
        logging.info("Fetching users...")
        members = fetch_users()

        # Step 2: Create Member Instances
        logging.info("Creating member instances...")
        member_data = create_members(members)

        # Step 3: Filter Mentors and mentorees
        logging.info("Filtering mentors and mentorees...")
        mentors, mentorees = filter_mentors_and_mentorees(member_data)

        # Step 4: Assign Mentorships
        logging.info("Assigning mentorships...")
        mentorships = assign_mentorships(mentors, mentorees)

        # Step 5: Normalize Data
        logging.info("Normalizing data into dataframes...")
        member_df, mentorship_df = normalize_data(member_data, mentorships)

        # Step 6: Calculate the median Age of Male Mentorees
        logging.info("Calculating median age of male mentorees...")
        median_age = median_age_of_male_mentorees(member_df, mentorship_df)
        logging.info(f"Median Age of Male Mentorees: {median_age}")

        # Step 7: Calculate the total Mentorees by Gender and Mentor Age
        logging.info("Calculating total mentorees by gender and mentor age...")
        gender_count = total_mentorees_by_gender_and_mentor_age(mentorship_df, member_df)
        logging.info(f"Mentorees by Gender and Mentor Age: {gender_count}")

        # Step 8: Check for Data Discrepancies across both dataframes
        logging.info("Checking for discrepancies in the data...")
        invalid_mentors, invalid_mentorees = check_discrepancies(member_df, mentorship_df)
        logging.info(f"Invalid Mentors: {invalid_mentors}")
        logging.info(f"Invalid Mentorees: {invalid_mentorees}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()