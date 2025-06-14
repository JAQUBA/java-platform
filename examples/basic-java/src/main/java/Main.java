import org.apache.commons.lang3.StringUtils;
import org.apache.commons.collections4.CollectionUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    
    public static void main(String[] args) {
        logger.info("Starting Java application with PlatformIO platform");
        
        // Demo użycia Apache Commons Lang
        String text = "Hello, PlatformIO Java Platform!";
        String reversed = StringUtils.reverse(text);
        logger.info("Original text: {}", text);
        logger.info("Reversed text: {}", reversed);
        
        // Demo użycia Apache Commons Collections
        List<String> list1 = new ArrayList<>();
        list1.add("Java");
        list1.add("PlatformIO");
        
        List<String> list2 = new ArrayList<>();
        list2.add("PlatformIO");
        list2.add("Maven");
        
        List<String> intersection = (List<String>) CollectionUtils.intersection(list1, list2);
        logger.info("List 1: {}", list1);
        logger.info("List 2: {}", list2);
        logger.info("Intersection: {}", intersection);
        
        // Demo informacji o JVM
        logger.info("Java Version: {}", System.getProperty("java.version"));
        logger.info("Java Home: {}", System.getProperty("java.home"));
        logger.info("Operating System: {}", System.getProperty("os.name"));
        
        logger.info("Application completed successfully!");
    }
}
