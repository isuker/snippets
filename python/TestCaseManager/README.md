    Test Manager

What's Test Manager(TM)
==================================
Test Central Portal for FQE. It's will replace HPQC and AutomatosX.


Test Manager Overview
==================================
TBD (Python + Flask + Celery)


RoadMap
==================================
Recent Features:

1. Test Case management (HIGH)
online test case add/edit/delete

2. Test Cycle management and report (HIGH)
Simiar with HPQC test cycle. TPAL can pull and drop all the test cases
to be executed for this test cycle, and assign different test cases in
this test cycle to test owners.

Testers post test reslut (should be automatos test log link) to TM.
TM will automatically generate one formal test result.

3. Intergate with Remedy. 
interative with Remedy through Remedy REST API. Auto file AR if possible.

4. user portal
User mangement is optional


Future Features:

1. Yet Another Automatos Frontend.
A AutomatosX killer. User can run automatos scipt on TM webpage.

2. Test device (array, hut, switch) management
FQE need a tool to simplfy set up test env. i.e intergrate enable/disable 
switch port. PowerCycle storage array and HUT.

Others
===================
Report Bugs or Suggestions to <ray.chen@emc.com>
