from importlib import metadata
import argparse


class RequirementsGenerator(object):
   def __init__(self, file_name: str) -> None:
      self.file_name: str = file_name


   def get_version(self, packets: list[str]) -> dict:
      result: dict = {}
      for packet in packets:
         try:
            result.update({packet: metadata.version(packet)})
         except metadata.PackageNotFoundError:
            print(f"[-] Could not find {packet}...")
      return result


   def read_file(self, file_name: str) -> list[str]:
      packets: list[str] = []
      try:
         with open(file_name, "r") as f:
            for line in f.readlines():
               packets.append(line.rstrip())
         return packets
      except FileNotFoundError:
         raise Exception("File not found error...")
         

   def requirements_file_generator(self, packets: dict) -> None:
      with open("requirements.txt", "w") as f:
         for index, packet in enumerate(packets):
            final: str  = "\n"
            if index == len(packets) - 1:
               final = final.rstrip()
            f.write(f"{packet}={packets[packet] + final}")


   def run(self) -> None:
      packets: list[str] = self.read_file(file_name)
      packets_version: dict = self.get_version(packets)
      self.requirements_file_generator(packets_version)


def get_arguments() -> str:
   parser = argparse.ArgumentParser()
   parser.add_argument("-f", "--file", dest="file", help="File name with the name of the libraries")
   options = parser.parse_args()
   if not options.file:
      file_name: str = str(input("Enter the name of the file with the name of the libraries: "))
      return file_name
   return options.file


if __name__ == "__main__":
   generator = RequirementsGenerator(file_name := get_arguments())
   generator.run()