package com.seat.esg.file;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;

@Controller
public class FileController {

    @GetMapping("/upload")
    public String upload() {
        return "upload";
    }

    @PostMapping("/upload")
    public String addFile(@RequestParam MultipartFile file) throws IOException {
        if (!file.isEmpty()) {
            String path = "./" + file.getOriginalFilename();
            file.transferTo(new File(path));
        }
        return "upload";
    }
}
