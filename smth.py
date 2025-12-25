# for num in range(35):
#     f = open(f"ubuntu/file{num}.txt", "w")
#     f.write("New file!\n")
#     f.close()

# with open("ubuntu/looongline.txt", "w") as file:
#     for i in range(10):
#         file.write(f"Line {i}\n")


for i in range(5):
    with open("ubuntu/looongline.txt", "r") as line:
        print(line.read())