package kr.co.littleriders.backend.domain.shuttle.service;

import kr.co.littleriders.backend.domain.shuttle.entity.ShuttleLocationHistory;

import java.util.List;

public interface ShuttleLocationHistoryService {

    ShuttleLocationHistory findByShuttleId(long shuttleId);

    boolean existsByShuttleId(long shuttleId);

    List<ShuttleLocationHistory> findAllByShuttleId(long shuttleId);

    void save(ShuttleLocationHistory location);

    void delete(ShuttleLocationHistory location);
}