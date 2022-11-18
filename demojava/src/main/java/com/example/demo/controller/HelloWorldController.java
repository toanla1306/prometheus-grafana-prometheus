package com.example.demo.controller;
import com.example.demo.mysql.DataSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

@RestController
public class HelloWorldController {

    @RequestMapping("/") // Nếu người dùng request tới địa chỉ "/"
    public String index()  throws SQLException {
        System.out.println("###################################");

        ArrayList<String> records = DataSource.fetchTestData();
        System.out.println("###################################");
        System.out.println(records);
        return "index test"; // Trả về file index.html
    }

}