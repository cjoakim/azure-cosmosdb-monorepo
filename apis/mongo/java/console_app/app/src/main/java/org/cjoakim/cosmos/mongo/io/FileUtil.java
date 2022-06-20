package org.cjoakim.cosmos.mongo.io;

import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Stream;
import java.nio.charset.StandardCharsets;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * Standard logic for reading various text, csv, and json files.
 *
 * @author Chris Joakim, Microsoft
 * @date   2022/06/20
 */

public class FileUtil {

    // Class variables
	private static Logger logger = LogManager.getLogger(FileUtil.class);

	public FileUtil() {
		
		super();
	}

	public String readText(String filename) throws Exception {

		byte[] encoded = Files.readAllBytes(Paths.get(filename));
		return new String(encoded, StandardCharsets.UTF_8);
	}

	public List<String> readFileLines(String filename) throws Exception {
		
		List<String> lines = new ArrayList<String>();
		Stream<String> stream = Files.lines(Paths.get(filename));
		stream.forEach(lines::add);
		return lines;
	}
	
	public List<Map> readCsvFile(String filename, boolean hasHeader, char delim) throws Exception {
		
		// see https://commons.apache.org/proper/commons-csv/user-guide.html
		Reader in = new FileReader(filename);
		List<Map> rows = new ArrayList<Map>();

		if (hasHeader) {
			Iterable<CSVRecord> records =
					CSVFormat.DEFAULT.withDelimiter(delim).withFirstRecordAsHeader().parse(in);
			for (CSVRecord record : records) {
				rows.add(record.toMap());
			}	
		}
		else {
			Iterable<CSVRecord> records =
					CSVFormat.DEFAULT.withDelimiter(delim).parse(in);
			for (CSVRecord record : records) {
				HashMap<String, String> row = new HashMap<String, String>();
				int size = record.size();
				for (int i = 0; i < size; i++) {
					String value = record.get(i);
					row.put("" + i, value);
				}
				rows.add(row);
			}
		}
		return rows;
	}
}
