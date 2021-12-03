package io.github.prrvchr.comp.tests;

import org.junit.runner.RunWith;
import org.junit.runners.Suite.SuiteClasses;

import io.github.prrvchr.comp.tests.base.UnoSuite;
import io.github.prrvchr.comp.tests.uno.WriterTest;

@RunWith(UnoSuite.class)
@SuiteClasses({WriterTest.class})
public class UnoTests {

}
