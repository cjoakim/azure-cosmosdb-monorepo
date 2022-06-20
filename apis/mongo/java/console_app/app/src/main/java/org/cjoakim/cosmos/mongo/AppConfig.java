package org.cjoakim.cosmos.mongo;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.ArrayList;

/**
 * Common configuration logic for command-line args and environment-variables.
 * Chris Joakim, Microsoft
 */

public class AppConfig implements AppConstants {

    // Class variables:
    protected static String[] commandLineArgs = new String[0];
    protected static Logger logger = LogManager.getLogger(AppConfig.class);

    /**
     * This method should directly or indirectly be invoked by the main() methods
     * in the dependent projects; pass it the command-line arguments passed to main().
     */
    public static void setCommandLineArgs(String[] args) {

        if (args != null) {
            commandLineArgs = args;
        }
    }

    public static String flagArg(String flagArg) {

        for (int i = 0; i < commandLineArgs.length; i++) {
            if (commandLineArgs[i].equalsIgnoreCase(flagArg)) {
                return commandLineArgs[i + 1];
            }
        }
        return null;
    }

    public static boolean booleanArg(String flagArg) {

        for (int i = 0; i < commandLineArgs.length; i++) {
            if (commandLineArgs[i].equalsIgnoreCase(flagArg)) {
                return true;
            }
        }
        return false;
    }

    public static long longFlagArg(String flagArg, long defaultValue) {

        try {
            return Long.parseLong(flagArg(flagArg));
        }
        catch (NumberFormatException e) {
            return defaultValue;
        }
    }

    public static boolean isVerbose() {

        return booleanArg(VERBOSE_FLAG);
    }

    public static boolean isSilent() {

        return booleanArg(SILENT_FLAG);
    }

    public static boolean isPretty() {

        return booleanArg(PRETTY_FLAG);
    }

    /**
     * Return the value of the given environment variable name.
     */
    public static String getEnvVar(String name) {

        return System.getenv(name);
    }

    /**
     * Return the value of the given environment variable name, defaulting to the
     * given defaultValue if the environment variable is not set.
     */
    public static String getEnvVar(String name, String defaultValue) {

        String s = getEnvVar(name);
        if (s == null) {
            return defaultValue;
        }
        else {
            return s;
        }
    }

}

