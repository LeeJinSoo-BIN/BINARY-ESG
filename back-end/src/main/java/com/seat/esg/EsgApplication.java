package com.seat.esg;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@EnableScheduling
@SpringBootApplication
public class EsgApplication {

	public static void main(String[] args) {
		SpringApplication.run(EsgApplication.class, args);
	}

}
