from .qnnna1 import check_similaritys

def runner():
      question1=[]
      question2=[]
      question1 = ['Where do you live',
                  'Where are you living',
                  'What is your age',
                  'Who is the president of USA',
                  'Which age is the best age to what get married?',
                  'How do I overcome my shyness with women?',
                  'Should Harry Potter have ended up with Cho Chang?',
                  'Where do macadamia nuts cost from?',
                  'Who is the nicest person you have ever met?',
                  'In do you say "closet" in French?',
                  'what is your mobile number',
                  'my company is apple',
                  'i like apple',
                  'i like apple',
                  ]

      question2 =['Where are you living',
                  'what are you doing',
                  'How old are you',
                  'Name the current president of USA',
                  'What is the best age to get for a woman?',
                  'How do you overcome being shy?',
                  'How powerful will Harry Potter become when he is grown up?',
                  'What the hangouts courses offered at AIIMS Bhopal?',
                  'Who was the weirdest classmate that you’ve ever met?',
                  'In French, how do get you say "cool"',
                  'which mobile number is you used',
                  'I work in apple',
                  'I work in apple',
                  'my favourite fruit is apple', 
                  ]

      a1 = ['what is your mobile number?',
      'Which model of mobile do you use?',
      'Have you taken your dinner',
      'who is the PM of Nepal',
      'what is CPU',
      'what type of coffee do you prefer',
      'Who is barbari',
      'Name of the main character of the Ramayan',
      'which ISP do you use',
            'How old are you',
            'how old are you'
      ]


      a2 = ['which mobile number is you used',
            'what is your mobiles model',
            'what meal do you eat at your dinner',
            'Name of the current PM of Nepal',
            'define CPU',
            'Which Coffee do you prefer to drink',
            'Name of the strongest character of Mahabharat',
            'Who is the main character of Ramayan',
            'which internet service provider do you use',
            'how good are you',
            'how age are you'
            ]

      question1+=a1
      question2+=a2
      scores=[]
      print(len(question1))
      for i in range(len(question1)):
            scores.append(check_similaritys(question2[i], question1[i]))

      for i in range(len(scores)):
            print(question2[i]," || ",question1[i]," -->>  ",scores[i])