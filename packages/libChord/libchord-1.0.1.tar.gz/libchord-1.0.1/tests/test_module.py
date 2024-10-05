import time
import unittest
from libChord import chord, node


class MyTestCase():

    def test_create(self):
        # self.assertEqual(True, False)  # add assertion here
        chord_obj = chord.Chord("Testing")
        chord_obj.listen()
        print(chord_obj.IP_ADDRESS)
        print(chord_obj.PORT)
        print("ID: ", chord_obj.node.id)

        while True:
            time.sleep(15)
            print(chord_obj.CHORD_DICT.items())
            print("SUCC ID: ", chord_obj.node.successor_id)
            print("PRED ID: ", chord_obj.node.predecessor_id)

            # command = int(input("Enter command: "))
            # if command == 0:
            #     pass
            # elif command == 1:
            #     print(chord_obj.CHORD_DICT.items())
            # elif command == 2:
            #     pass
            # elif command == 3:
            #     print("SUCC ID: ", chord_obj.node.successor_id)
            # elif command == 4:
            #     print("PRED ID: ", chord_obj.node.predecessor_id)
            # elif command == 5:
            #     chord_obj.node.leave()
            # else:
            #     break

            # print(self.chord_obj.central_hub)
            # print(chord_obj.NETWORK_NAME)
            # print(chord_obj.node.node_keySpace)


    def test_display(self):
        pass

    def test_join(self):
        pass


if __name__ == '__main__':
    obj = MyTestCase()
    obj.test_create()

