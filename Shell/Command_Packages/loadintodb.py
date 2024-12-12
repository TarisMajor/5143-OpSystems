from .dbCommands import DbCommands

db_path = './P01/ApiStarter/data/filesystem.db'

def loadintodb(**kwargs):
    
    name = "Pooh.txt"
    
    pid = "44"
    
    content = """
    **Winnie the Pooh: A Timeless Tale of Friendship and Adventure**

    Winnie the Pooh, the beloved bear of very little brain, is a character that has enchanted children and adults alike for generations. Created by A.A. Milne, Pooh's adventures in the Hundred Acre Wood are full of warmth, whimsy, and wonder. This essay explores Pooh’s story, incorporating words that begin with each letter of the alphabet, showcasing the magic of this timeless classic.

    **A**lthough Pooh is often seen as a simple bear, his **adventures** are anything but dull. He is surrounded by a cast of friends who each contribute to the richness of the stories. Pooh’s closest companion, **Piglet**, is a small, timid pig who is always ready to offer support. Together, they navigate the **challenges** of life with heartwarming humor and **courage**.

    In the Hundred Acre Wood, every **day** is a new opportunity for exploration. Pooh and his friends are often seen **enjoying** simple pleasures, such as **eating** honey or playing games. The central theme of the stories is **friendship**, a powerful force that binds the characters together. **Generosity** and kindness shine through in their interactions, reminding readers of the importance of helping one another.

    One of Pooh’s most endearing qualities is his **honesty**. Despite his lack of intelligence, he always speaks from the heart. He has a natural **innocence** that makes him relatable to both children and adults. Pooh’s **jovial** nature and **kind-hearted** spirit make him a character who never fails to bring joy.

    The world of Winnie the Pooh is also **known** for its beautifully detailed setting. The trees, flowers, and paths of the Hundred Acre Wood are always described in a way that makes readers feel as if they are there, walking alongside Pooh and his friends. Milne’s **language** captures the charm and **magic** of this world, inviting the imagination to run wild.

    Pooh’s love for honey is a symbol of his **persistent** and often **quirky** nature. Whether he’s climbing trees to steal a pot of honey or pondering a riddle, Pooh’s thoughts are always delightful. His **quiet** moments of reflection often lead to profound insights, and his **resourcefulness** helps him find solutions to problems, even when the answers seem unclear.

    Even in moments of **sadness**, Pooh’s friends rally around him, proving that true friendship transcends any adversity. Characters like **Rabbit**, **Tigger**, and **Eeyore** all bring something unique to the group. **Tigger**, with his **tireless** energy and exuberance, provides contrast to Pooh’s more laid-back style, while **Eeyore**’s **melancholy** outlook on life often serves as a reminder of the need for empathy and care.

    The beauty of the stories lies in their **universality**. Children can relate to the playful escapades, while adults can appreciate the deeper meanings embedded in the tales. The sense of wonder that the stories evoke is what makes them **timeless**. Pooh’s **understanding** of the world, despite his occasional confusion, offers wisdom that continues to resonate with readers.

    In conclusion, the adventures of **Winnie the Pooh** are not just stories of a bear and his friends; they are lessons in life. Through their **varied** personalities and unique perspectives, the characters teach valuable lessons about **love**, **loyalty**, and the **importance** of cherishing the simple things in life. From **A** to **Z**, the Hundred Acre Wood is a world full of **adventure**, where every reader can find something to smile about.
    """
    
    results = DbCommands.new_file(db_path, name, content, pid)
    print(results)