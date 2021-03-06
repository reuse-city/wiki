# E-I - evaluation interface

![](header.jpg)

## Description

**E-I** is technology (hardware + software) to increase the ability to reuse products and materials.

Drafting a basic prototype:

- User shows an object to E-I
- E-I compares images and other information collected from the product/object (weight, colors, barcode, QR code) against a database such as the [universal registry of things](../universal-registry/README.md)
- When information about the object is found, E-I retrieves it and delivers to the user
- When information about the object is not found, E-I allows the user to input information

For prototyping purposes, mock-ups of a workbench version of E-I can be constructed:

- With an articulated arm, a NFC sensor + arduino (playing with code [here](NFC)), and a screen showing a local website (running off a server in a Raspbery Pi). NFC tags are added to pre-selected products.
- With an articulated arm, a Raspberry Pi with a camera and screen, and computer vision software to recognise predefined objects (different colors, maybe). Here's a start on its shape in [a workbench setup](https://www.youtube.com/watch?v=VU87-ANYerk). Can [teachable machine](https://teachablemachine.withgoogle.com/) be used perhaps?
- With an articulated arm, a Raspberry Pi with camera, screen, microphone and speaker. The user can interact with E-I both via the camera and voice commands / feedback.

![E-I - short video description](prototype_E-I.mkv)

## Sketch #1

![E-I Workbench number 1](20210423_E-I_workbench.png)

**Expected behaviour:**

1. Put an object in the mat. The proximity sensor turns the LCD on. A welcome screen is shown. Button to start E-I on the screen.
2. Button is clicked: camera is turned on and shows an image of what is in the mat. Overlay message "scanning for things" (or "objects", or "materials"?).
3. Once an object is recognised (for prototyping purposes, via NFC), show message on screen (optionally, sound a notification - but that needs a speaker too)
	1.  Case A: known object. Overlay message: "Object found on database". Buttons on screen:
		1.  What is this -> navigate to page with description of object (video, images, text, other info)
		2.  What can I do with this -> navigate to page with information about repair, upcycling, re-circulation, second hand market value
	2.  Case B: unkown object. Overlay message: "Object not yet on database". Button says "Add this to the universal registry of things". Click -> page with form (need to add a keyboard as well). Ability to take picture or shoot video with E-I's camera.

![Unicorn](20210423_unicorn.jpg)

## This prototype

The goal with E-I at this point is not to develop a functional product, but rather to experiment with speculative use cases in order to discuss how  technologies might help interested parties reuse a larger proportion of materials that are currently discarded or kept out of use.  Other points of discussion are what would the implications of such technologies be in terms of use, privacy, health and safety, policy and economy.

Original concept:  [Point and Reuse](https://is.efeefe.me/concepts/point-reuse), created in previous phases of research.

![](valooe.png)

## References

### [Monk - Ai-based inspection system](https://monkvision.ai/#how-it-works)

> Creating Trust whenever an item changes hands.

Repository [here](https://github.com/Tessellate-Imaging/monk_v1).

### [Formation "Agent valoriste"](https://ecossolies.fr/Formation-Agent-valoriste)

> Les professionnel.les du secteur du r??emploi et du recyclage exercent des m??tiers vari??s : agent valoriste, chauffeur collecte, responsable boutique, op??rateur de tri, vendeur ??? Chaque jour, ces professionnel.les contribuent ?? d??tourner de l???incin??rateur des m??tres cubes de mati??res. Leur r??le est aussi essentiel pour amener les citoyens et les entreprises ?? adopter des r??flexes et des pratiques responsables en mati??re de tri et de consommation.
> Depuis 5 ans, les Ecossolies en lien avec les acteurs ESS du secteur ?? R??emploi/Ressources ??, forment des professionnels du secteur autour des principales fonctions du m??tier de valoriste :
>  - Collecter, trier, valoriser des objets, des mati??res
>  - Informer, orienter, sensibiliser aux enjeux du r??emploi
>  - Travailler en r??seau avec les acteurs agissant dans la pr??vention et la gestion des d??chets.
> Les participants de la formation peuvent aussi bien ??tre des agents op??rateurs terrain, que des ??quipes d???encadrement et travaillent dans des fili??res d???activit??s diff??rentes (textile, D3E, BTP, ??lectro-m??nager), et au sein de diff??rentes structures : ressourceries, structure d???insertion, collectivit??s locales, associations de quartiers.
