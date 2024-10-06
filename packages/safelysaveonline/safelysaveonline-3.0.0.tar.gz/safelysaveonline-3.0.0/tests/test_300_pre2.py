import os
import shutil
import safelysave

if os.path.isfile('test-file.sso'):
    os.remove('test-file.sso')

repo = input('[Enter git repository] ')

key = safelysave.create_sso_file('test-file.sso', 'git', repo)

content = {
    "test": "check",
    "test2": "check2",
    "uuid": 'failed'
}
content2 = {
    "test3": "check3",
    "test4": "check4",
    "uuid": 'failed'
}

ssoinstance = safelysave.sso('test-file.sso', key)

ssoinstance.add_data(content)
ssoinstance.add_data(content2)

data = ssoinstance.get_data()

ssoinstance.remove_data(data[1]['uuid'])

data = ssoinstance.get_data()

passed = 0
print("")

if len(data) == 1:
    print("Passed Test 1")
    passed += 1
else:
    print("Failed Test 1 (No or 2+ entries existing.)")

if data[0]['test'] == 'check':
    print("Passed Test 2.1")
    passed += 1
else:
    print("Failed Test 2.1 (Entry is not valid.)")

if data[0]['test2'] == 'check2':
    print("Passed Test 2.2")
    passed += 1
else:
    print("Failed Test 2.2 (Entry is not valid.)")

if data[0]['uuid'] != 'failed':
    passed += 1
    print("Passed Test 2.3")
else:
    print("Failed Test 2.3 (Did not overwrite UUID.)")

ssoinstance.sync()
data = ssoinstance.get_data()

print("Synced with git.")

if len(data) == 1:
    print("Passed Test 3")
    passed += 1
else:
    print("Failed Test 3 (No or 2+ entries existing.)")

if data[0]['test'] == 'check':
    print("Passed Test 4.1")
    passed += 1
else:
    print("Failed Test 4.1 (Entry is not valid.)")

if data[0]['test2'] == 'check2':
    print("Passed Test 4.2")
    passed += 1
else:
    print("Failed Test 4.2 (Entry is not valid.)")

if data[0]['uuid'] != 'failed':
    passed += 1
    print("Passed Test 4.3")
else:
    print("Failed Test 4.3 (Did not overwrite UUID.)")

ssoinstance.overrite_file('data', [])

if len(data) == 1:
    print("Passed Test 5")
    passed += 1
else:
    print("Failed Test 5 (An entry exists after overwrite.)")

print("")
print(f'[Result] Passed {passed}/9 tests.')
