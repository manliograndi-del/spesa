# -*- coding: utf-8 -*-
"""Gli indirizzi delle pagine del volantino Aldi, uno per uno.

Aldi pubblica il volantino su Publitas (`volantino.aldi.it/<nome>/`), il suo
sito ufficiale per i volantini. Ogni pagina ha un'immagine con un codice suo
nell'indirizzo: il numero di pagina da solo non basta, quindi gli indirizzi
si tengono qui, in ordine (il primo è la pagina 1).

**Vanno rifatti a ogni volantino nuovo.** Si prendono da
`https://volantino.aldi.it/<nome>/spreads.json`: per ogni pagina, `number` e
`images.at1600`, da mettere dopo `https://view.publitas.com`. Il nome del
volantino in corso lo dice `https://volantino.aldi.it/` (rimanda a quello
nuovo). Lo stesso file ha anche il testo di ogni pagina (`text`).
"""

# «Offerte da lunedì 28 settembre», 34 pagine
PAGINE_ALDI_28 = [
    'https://view.publitas.com/resize/rev-95488569/sPL6GVzFGit8NM01Qgle0YldWCz3hYjPhSPhJ4-wLA4/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/4d283c2f-23ec-4791-8996-837717c59285-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/mo-J2zaNQtPjDuMk99soAZJXxeqADj2fkWt6gJKekqs/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/0c365640-6a6e-451f-9422-11e23acfb57f-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/Z4SrbXMJ5bH-uzh5gkon4M8ObxDlkWtxbY93thv3EGw/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/e47f284b-8305-4ec3-a3b7-f692e7f86f0f-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/q0J4_SiNP0gStwVViYGYtUAFMISLeMlceANtp2qf_Q4/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/f7dbd2c4-0d47-4609-9f06-58691e7308cd-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/SLSiNgb4I13OZ-C2Na0qyPTgl2oS-cl_tQsjr4srBzA/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/9f1e4192-b99c-4b87-a0a9-e6e145f42d06-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/7dv9hOmuK9H4E8Os0beYEpCDDJuWQLGQZp1LYHSMPcc/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/705f0b04-8d0b-48fa-a8b3-f3662c8cc371-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/pF6LLYUs7yOJ0vO0NhnherkWY3g9uHcviCVWZu6C_JU/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/f1730eea-8d44-4f46-8e6a-a3be5dece123-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/RVM-tIqSQOuoXNktjfLo1kM577ECj0z_IwWAIZ5qrZs/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/766bdd35-dd49-4d7d-b18f-312e92e74683-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/knYXWua-Z5JE1C-4onn9U4HLsJsiG0PTigQZPQ9L4pk/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/31dbba77-4c1e-4478-b3f2-da1ee72adc58-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/RuiUmTL7DFgGrU6XE88kH3XB9WMfTxkNZYPvrp_bf10/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/3d0a136d-ff94-4092-b514-7f3ac7f1d4e4-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/D0lJN00hj-5jsJPjB4_A_2ExzhJblq67itAmMQgSWAE/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/ddad7c7d-ccb3-4f7c-81ac-b85660dcf304-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/MumhLSYf7fmohy-H4BWl_KrZUWNpuB5-u-bC8aDvj8A/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/64cae254-ef51-453f-ba1c-dfff7ecbfbbb-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/9eS26OJnXDBbI3wieU1V-AFEG4Ez1xKiZLGElouK4NA/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/f930d7c6-7636-431e-9e5b-b452e0b33da9-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/9HmT8aSfR7uHv9gUVMu6_6RfFJUmBls2zbrNE8ygIIs/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/4f54e18f-8f11-4196-b9a9-96306b50a92f-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/R2YBjQ4O7TzD0l_z8ChZUxw5dgxaGqTDQepTycCuNDg/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/497f5711-f118-4e59-9737-45013a0e7e12-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/7-ENTCJ3fbjZ0NZstQ2Xgn_vjN8omH7V8Et7pcsLsLs/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/62068aaa-9a27-4d3a-a813-451ca543e26a-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/jU8zx7nEODW4jLBmCDzb2AG0SdkOSIXQnk8MQUDHvNY/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/2ff998dc-113d-4d57-a3d6-9a25c1251cf6-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/CppGHZIFNHde3b6ykai9XNi53k0piVBwj9bzkUOseCo/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/b135e76c-811b-43a1-bfd2-43df9559609a-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/BtPGmOKVqa_YLdR4Rf7uOdRn8x8aFvLdvlMxwtUbaDA/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/0750eeb4-6dd5-4ad3-88f5-adfdfe8d2a70-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/aD26YqQ5387XX8-5o1FzUFj87xRdZZobRxAqlndLpSQ/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/48d75126-d8dd-4223-b863-1294fbfe93d0-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/uyVPrXCEVu5jj40gP5y3-bu7hgudaMW-45H4vspzmQg/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/d62db468-ea87-4d1d-9818-0ed845c9c1c4-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/Gqk2OaHxhOoW5pLbtExaSUsJ8RDSc9YeBdxzV1WqdFg/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/e4c319cc-bf18-401a-bf4d-74e4e80fc20a-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/P8E9lEU-SwxYUAU3wqHcI8lwm7jugfhxZMmtN-NCuXQ/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/d7fcbd9a-33e9-4e43-ba44-01746ddace83-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/_kbvWeyGBFysTZ1bFO6dTuQCvBPZ-HJh5f_ssZdtdrU/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/c9a533ac-4482-4f12-974a-191a5e249cac-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/ImboyeAq0BK20DJHcwHOH8dIFR-SaLN7lqPAj0RkiWQ/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/6ed893fb-f567-4c03-b06c-e09e07123838-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/mlrZX-ecSBFiNUbNO1OBJTlTbWHuvdJJW1L4NvWv26U/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/3871ff9b-b6f2-4159-aa6c-0874acdc7667-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/Qqq4zBFeShOuDlB4qpzRNctIDBgEpIS8B3UuAXgh_dA/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/656028f5-f476-464e-9ded-ec2935f03f37-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/augqCeEg1rvMUyS7kTVZnzG3epwNj5gglftXkUozt2E/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/039e378e-8245-44ea-aae9-c4460af7d4c8-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/JRfiPZQUQNEDboWSoK_Wk5zhRyfqxnnyiaEnhJfqdpk/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/eab62e7b-0ac4-4a8e-890e-78cde5e67e4a-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/5h2d8B2jWTAMePPg9S9qgzmX7FdMAqL340tj1CPhLIs/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/b9cf909a-2058-410e-977a-26151a0529f4-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/NKGda34wbH06Kt2PtQp9gGAI66yqaj-dP3OEmkFDl5o/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/f6a602f9-da7a-431a-8981-f16987224262-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/Q4tsxDuezhc7f1UFw6W3CcTMq-lZJlTMXPEVYuP-RDI/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/bf8adb8b-68ab-4622-b4d8-8fc1bdfd5573-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/qX6oP_-R0tZn1dQpkfOjcptIJq9wQ1V7r6DaPr1EYg0/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/ee6d874f-1c7e-4f13-a876-b818e1630145-downscaled.jpg',
    'https://view.publitas.com/resize/rev-95488569/xlj5qN9kJ-s7HjFj9JP0gz2aCEhRExrT36_WuB5_xxA/fit-in/1228x2084/filters:quality(90)/production-revolution-publitas-com/96382/3361994/pages/eee26312-33e5-46b8-afc9-12b43a19f327-downscaled.jpg',
]
