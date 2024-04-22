package kr.co.littleriders.backend.domain.childhistory;

import java.time.LocalDate;
import java.time.LocalDateTime;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import kr.co.littleriders.backend.domain.Gender;

@Entity
public class ChildHistory {

	@Id
	private Long id;

	// private Child child;

	private String name;

	private LocalDate birthDate;

	private Gender gender;

	private String imagePath;

	private LocalDateTime createdAt;


}
