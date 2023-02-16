CIFILE = intermediate_tests/test1.ci;
TESTFILE = cimple.test.intermediate.py

CC = python3
INPUT = cimple.py
DELFILES = __pycache__ ./**/__pycache__ ./*.c ./**/*.c ./*.int ./**/*.int ./*.out ./**.out

run:
	$(CC) $(INPUT) $(CIFILE)

test:
	$(CC) $(TESTFILE)

testall:
	$(CC) cimple.test.parser.py
	$(CC) cimple.test.final.py
	$(CC) cimple.test.intermediate.py

clean:
	$(RM) -r $(DELFILES)
