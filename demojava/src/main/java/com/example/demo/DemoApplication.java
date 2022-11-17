package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoApplication {

	public static void main(String[] args) {
		// PrometheusMeterRegistry prometheusRegistry = new PrometheusMeterRegistry(PrometheusConfig.DEFAULT);
        // try {
        //     HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
        //     server.createContext("/prometheus", httpExchange -> {
        //         String response = prometheusRegistry.scrape();
        //         httpExchange.sendResponseHeaders(200, response.getBytes().length);
        //         try (OutputStream os = httpExchange.getResponseBody()) {
        //             os.write(response.getBytes());
        //         }
        //     });
        //     new Thread(server::start).start();
        // } catch (IOException e) {
        //     throw new RuntimeException(e);
        // }
		SpringApplication.run(DemoApplication.class, args);
		
	}

}
