# RR demo
This is a sample project with RR https://rr-project.org/ using gnatstudio that works out of the box. And provides som simple extra features in gnatstudio for debugging using rr.
## Setup
* Enable necessary traces in the kernel and enable the plug-in. `make setup`

* Try to catch the bug.  `make record`

* Finally start debugging the recorded sesion.
  * start GPS
  * <menue>/Debug/rr/initialze replay
  * Do normal debugging, with the extra reverse stepping facilities and the capability of re-run the execution with new break and watch points.

