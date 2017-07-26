/*
 * Created on 19-01-2005
 */
package org.aspectj.systemtest;

import junit.framework.Test;
import junit.framework.TestSuite;

import org.aspectj.systemtest.ajc170.AllTestsAspectJ170;

public class AllTests17 {

	public static Test suite() {
		TestSuite suite = new TestSuite("AspectJ System Test Suite - JDK 1.7");
		// $JUnit-BEGIN$
		suite.addTest(AllTestsAspectJ170.suite());
		suite.addTest(AllTests16.suite());
		suite.addTest(AllTests15.suite());
		// $JUnit-END$
		return suite;
	}
}
