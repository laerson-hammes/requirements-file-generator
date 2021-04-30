from typing import List, Dict
from importlib import metadata
import argparse


class RequirementsGenerator(object):
   def __init__(self, /) -> None:
      self.run()


   def get_version(self, packets: List[str], /) -> Dict:
      result: Dict = {}
      for packet in packets:
         try:
            result.update({packet: metadata.version(packet)})
         except metadata.PackageNotFoundError:
            print(f"[-] Could not find {packet}...")
      return result


   def read_file(self, file_name: str, /) -> List[str]:
      packets: List[str] = []
      try:
         with open(file_name, "r") as f:
            for line in f.readlines():
               packets.append(line.rstrip())
         return packets
      except FileNotFoundError:
         raise Exception("File not found error...")
         

   def requirements_file_generator(self, packets: Dict, /) -> None:
      with open("requirements.txt", "w") as f:
         for index, packet in enumerate(packets):
            final: str  = "\n"
            if index == len(packets) - 1:
               final = final.rstrip()
            f.write(f"{packet}={packets[packet] + final}")


   def run(self, /) -> None:
      packets: List[str] = self.read_file(self.get_arguments())
      packets_version: Dict = self.get_version(packets)
      self.requirements_file_generator(packets_version)


   def get_arguments(self, /) -> str:
      parser = argparse.ArgumentParser()
      parser.add_argument("-f", "--file", dest="file", help="File name with the name of the libraries")
      options = parser.parse_args()
      if not options.file:
         return str(input("Enter the name of the file with the name of the libraries: "))
      return options.file


if __name__ == "__main__":
   generator = RequirementsGenerator()