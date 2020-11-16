# Cloud Architecture - Assignment 1

- Institution: Waterford Institute of Technology
- Program: MSc in Computing (Enterprise Software Systems)
- Module: Cloud Architecture 2020/2021
- Student: Amador Pahim Segundo
- Screencast: [https://www.youtube.com/watch?v=nWvrR08RBHk](https://www.youtube.com/watch?v=nWvrR08RBHk)

This repository contains all the artifacts produced for the Assignment 1 of the
Cloud Architecture module:

- [README.md](README.md): this file, containing general information about this
  repository.
- [WIT_CloudArchitecture_Assignment1_AmadorPahim.md](WIT_CloudArchitecture_Assignment1_AmadorPahim.md):
  final report in MarkDown format.
- [WIT_CloudArchitecture_Assignment1_AmadorPahim.pdf](WIT_CloudArchitecture_Assignment1_AmadorPahim.pdf):
  final report exported to PDF.
- [Assignment1GradingRubric.xlsx](Assignment1GradingRubric.xlsx):
  spreadsheet with the gradings rubric.
- [App/](App/): the custom web application crated for the Assignment 1.
- [CloudFormation/](CloudFormation/): directory containing the Cloud Formation
  Stack that captures all the AWS resources of the Assignment 1.
- [Diagrams/](Diagrams/): source code of the diagrams in XML format.
- [Img/](Diagrams/): screeshots and diagrams exported to PNG.
- [Lambda/](Lambda/): the Lambda function source code. 
- [LoadTest/](LoadTest/): the load test scripts. 
- [UserData/](UserData/): the scripts used as "User Data" to bootstrap the EC2
  instances.

## Export Documentation to PDF

Install pandoc:
```bash
$ pip install pandoc
```

Export with:

```
$ pandoc -t pdf \
-o WIT_CloudArchitecture_Assignment1_AmadorPahim.pdf \
-V geometry:margin=1in \
WIT_CloudArchitecture_Assignment1_AmadorPahim.md
```

## Run the Load Test

Install locust:

```bash
$ pip install locust
```

Run:

```
$ locust -f LoadTest/WebServerLoadTest.py
```

Add the web application URL and the number of users you want to simulate.
