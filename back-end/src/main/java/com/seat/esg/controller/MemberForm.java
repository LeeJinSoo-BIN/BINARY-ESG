package com.seat.esg.controller;

import com.seat.esg.domain.MemberRole;
import lombok.Getter;
import lombok.Setter;

import javax.validation.constraints.NotEmpty;

@Getter @Setter
public class MemberForm {

    @NotEmpty(message = "회원 이름을 입력하세요.")
    private String name;
    @NotEmpty(message = "비밀번호를 입력하세요.")
    private String password;
//    private MemberRole role;
}
