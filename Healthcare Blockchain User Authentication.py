# -*- coding: utf-8 -*-
"""
Created on Sat Aug  2 22:09:00 2025

@author: ashai
"""

import hashlib
import time
import json
import getpass

# Simple user database (for demo purposes)
USERS = {
    "doctor": "docpass",
    "nurse": "nursepass",
    "admin": "adminpass"
}

def authenticate_user():
    print("=== Healthcare Blockchain User Authentication ===")
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    if USERS.get(username) == password:
        print(f"Access granted. Welcome, {username}!\n")
        return True
    else:
        print("Invalid username or password.\n")
        return False

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # healthcare record dict
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class HealthcareBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # Initial block with no data
        return Block(0, time.time(), {"info": "Genesis Block"}, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        latest_block = self.get_latest_block()
        new_index = latest_block.index + 1
        new_timestamp = time.time()
        new_previous_hash = latest_block.hash
        new_block = Block(new_index, new_timestamp, data, new_previous_hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                print(f"Invalid hash at block {i}")
                return False
            if current.previous_hash != previous.hash:
                print(f"Invalid previous hash at block {i}")
                return False
        return True

    def save_to_file(self, filename):
        data = []
        for block in self.chain:
            data.append({
                'index': block.index,
                'timestamp': block.timestamp,
                'data': block.data,
                'previous_hash': block.previous_hash,
                'hash': block.hash
            })
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Blockchain saved to {filename}")

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)

        loaded_chain = []
        for block_data in data:
            block = Block(
                block_data['index'],
                block_data['timestamp'],
                block_data['data'],
                block_data['previous_hash']
            )
            block.hash = block_data['hash']  # preserve stored hash
            loaded_chain.append(block)

        self.chain = loaded_chain
        print(f"Blockchain loaded from {filename}")

def display_blockchain(blockchain):
    print("\n=== Healthcare Blockchain ===")
    for block in blockchain.chain:
        print(f"Block Index: {block.index}")
        print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block.timestamp))}")
        print("Data:")
        for key, value in block.data.items():
            print(f"  {key}: {value}")
        print(f"Hash: {block.hash}")
        print(f"Previous Hash: {block.previous_hash}")
        print("-----------------------------")
    print(f"Blockchain valid? {blockchain.is_chain_valid()}\n")

def main():
    if not authenticate_user():
        print("Authentication failed. Exiting.")
        return

    blockchain = HealthcareBlockchain()

    while True:
        print("Choose an option:")
        print("1. Add new patient record")
        print("2. Add new test result")
        print("3. Add new prescription")
        print("4. Add new appointment")
        print("5. Add new vaccination record")
        print("6. Display blockchain")
        print("7. Save blockchain to file")
        print("8. Load blockchain from file")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ").strip()

        if choice == '1':
            patient_id = input("Patient ID: ")
            name = input("Patient Name: ")
            age = input("Age: ")
            gender = input("Gender: ")
            address = input("Address: ")
            data = {
                "type": "Patient Record",
                "patient_id": patient_id,
                "name": name,
                "age": age,
                "gender": gender,
                "address": address,
                "recorded_at": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            }
            blockchain.add_block(data)
            print("Patient record added!\n")

        elif choice == '2':
            patient_id = input("Patient ID: ")
            test_type = input("Test Type (e.g., Blood, X-Ray): ")
            results = input("Results: ")
            doctor = input("Doctor Name: ")
            data = {
                "type": "Test Result",
                "patient_id": patient_id,
                "test_type": test_type,
                "results": results,
                "doctor": doctor,
                "recorded_at": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            }
            blockchain.add_block(data)
            print("Test result added!\n")

        elif choice == '3':
            patient_id = input("Patient ID: ")
            medication = input("Medication: ")
            dosage = input("Dosage: ")
            frequency = input("Frequency: ")
            prescribing_doctor = input("Prescribing Doctor: ")
            data = {
                "type": "Prescription",
                "patient_id": patient_id,
                "medication": medication,
                "dosage": dosage,
                "frequency": frequency,
                "prescribing_doctor": prescribing_doctor,
                "recorded_at": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            }
            blockchain.add_block(data)
            print("Prescription added!\n")

        elif choice == '4':
            patient_id = input("Patient ID: ")
            appointment_date = input("Appointment Date (YYYY-MM-DD): ")
            doctor = input("Doctor: ")
            reason = input("Reason for Appointment: ")
            data = {
                "type": "Appointment",
                "patient_id": patient_id,
                "appointment_date": appointment_date,
                "doctor": doctor,
                "reason": reason,
                "recorded_at": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            }
            blockchain.add_block(data)
            print("Appointment record added!\n")

        elif choice == '5':
            patient_id = input("Patient ID: ")
            vaccine = input("Vaccine Name: ")
            dose_number = input("Dose Number: ")
            vaccination_date = input("Vaccination Date (YYYY-MM-DD): ")
            administered_by = input("Administered By: ")
            data = {
                "type": "Vaccination Record",
                "patient_id": patient_id,
                "vaccine": vaccine,
                "dose_number": dose_number,
                "vaccination_date": vaccination_date,
                "administered_by": administered_by,
                "recorded_at": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            }
            blockchain.add_block(data)
            print("Vaccination record added!\n")

        elif choice == '6':
            display_blockchain(blockchain)

        elif choice == '7':
            filename = input("Enter filename to save (e.g., healthcare_blockchain.json): ")
            blockchain.save_to_file(filename)

        elif choice == '8':
            filename = input("Enter filename to load (e.g., healthcare_blockchain.json): ")
            try:
                blockchain.load_from_file(filename)
            except FileNotFoundError:
                print("File not found. Please check the filename.\n")

        elif choice == '9':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice, please try again.\n")

if __name__ == "__main__":
    main()
