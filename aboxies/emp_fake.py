from faker import Faker
fake = Faker('pt_BR')

def main():
  for e in range(5):
    e = fake.company()
    print(e)



if __name__ == "__main__":
  main()
