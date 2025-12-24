# print('hwjhsd')
import sys
# print("RAW ARGV:", sys.argv[2])
j = sys.argv[2]
print(j)
error = j['error']
command = j['command']
sh = j['shell']

print(error , command , sh)
# import argparse
# import json
# print('here1')
# parser = argparse.ArgumentParser()
# parser.add_argument("--payload", required=True)
# print('here2')
# args = parser.parse_args()
# print('here3')
# data = json.loads(args.payload)

# print("\n--- LLM ASSIST DEBUG ---")
# print("Command:", data["command"])
# print("Error:", data["error"])
# print("Shell:", data["shell"])
# print("------------------------\n")
