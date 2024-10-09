import hanifx

# ব্যবহারকারীর ইনপুট নিন
data = input("Enter data to hash using hanifx: ")

# hanifx মডিউলের enc ফাংশন ব্যবহার করুন
hashed_value = hanifx.enc(data)

print(f"Hashed Value: {hashed_value}")
