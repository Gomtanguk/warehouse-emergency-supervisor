# warehouse-emergency-supervisor

Isaac Sim과 ROS 2를 함께 사용하는 창고 사고 대응 시뮬레이션 프로젝트입니다. 드론 순찰, 바코드 스캔, 가스 사고 감지, 모바일 매니퓰레이터 출동, 밸브 조작 시퀀스를 하나의 슈퍼바이저 스크립트로 통합합니다.

## Quick Summary

- Domain: 창고 사고 대응 슈퍼바이저 시뮬레이션
- Stack: Isaac Sim, ROS 2 Humble, Python, USD, Action Graph
- Key Entry Point: `integrated_warehouse_supervisor_v6.py`

## 구조

```text
warehouse-emergency-supervisor/
├── docs/
│   ├── *.mp4
│   ├── *.pdf
│   └── *.pptx
├── src/
│   └── warehouse_emergency_supervisor/
│       ├── integrated_warehouse_supervisor_v6.py
│       ├── package.xml
│       ├── setup.py
│       ├── setup.cfg
│       ├── resource/
│       ├── custom_mobile/
│       ├── barcodes/
│       ├── *.usd
│       ├── map.yaml
│       └── map.png
└── README.md
```

## 구성 요소

- `integrated_warehouse_supervisor_v6.py`
  - 메인 엔트리포인트
- `custom_mobile/`
  - 모바일 매니퓰레이터 보조 모듈
- `barcodes/`
  - 바코드 자산
- `*.usd`
  - Isaac Sim 환경 및 로봇 자산
- `map.yaml`, `map.png`
  - 출동용 지도 자산

## 패키지 상태

- 현재 저장소는 `ament_python` 패키지 메타파일을 포함합니다.
- 패키지명은 `warehouse_emergency_supervisor`입니다.
- 실행 엔트리포인트는 `warehouse_supervisor = integrated_warehouse_supervisor_v6:main`으로 등록되어 있습니다.

## 실행 개념

- 가스 사고 시작 토픽을 받으면 사고 구역을 선택합니다.
- 드론이 사고 지점으로 출동하고 필요한 정보를 발행합니다.
- 모바일 매니퓰레이터가 목표 지점으로 이동해 밸브 조작 시퀀스를 수행합니다.
- Action Graph 신호와 ROS 토픽을 동기화하며 상태를 전이합니다.

## 알고리즘 개요

### 1. 사고 구역 선택과 상태 전이

- 가스 사고 시작 토픽을 받으면 A/B/C/D 중 사고 구역을 선택합니다.
- 내부 FSM이 평상시, 사고 감지, 드론 출동, 모바일 작업, 복구 상태로 전이합니다.
- 각 구역 상태는 ROS 토픽과 Action Graph 상태 코드로 함께 관리됩니다.

### 2. 드론 순찰과 이벤트 디스패치

- 드론은 미리 정의된 순찰 포인트를 따라 이동하며 바코드 스캔을 수행합니다.
- 사고가 발생하면 기본 순찰을 중단하고 override 모드로 사고 구역에 긴급 출동합니다.
- 도착 후 모바일 로봇이 사용할 출동 좌표를 계산해 ROS 토픽으로 발행합니다.

### 3. 모바일 로봇 경로 계획

- 지도 파일 `map.yaml`, `map.png`를 기준으로 목표 지점까지 경로를 계산합니다.
- 기본 경로 계획은 A* 기반이며, 근접 구간에서는 반응형 회피와 정렬 로직을 섞어 사용합니다.
- 목표 지점에 도달하면 도착 이벤트를 발행하고 작업 단계로 넘어갑니다.

### 4. 매니퓰레이터 작업 시퀀스

- 매니퓰레이터는 접근, 그립, 회전, 해제, 복귀 순서로 밸브 조작 시퀀스를 수행합니다.
- 각 단계는 시간 기반 보간으로 연결되어 순간이동처럼 보이지 않도록 스무스 모션을 사용합니다.
- 밸브 상태는 시뮬레이션 내부 자산과 ROS 토픽에 동시에 반영됩니다.

### 5. 자동 정상화

- 밸브 차단 이후 ppm 감소를 시뮬레이션하고, 농도가 0에 가까워지면 자동으로 Normal 상태로 전환합니다.
- 타임아웃이나 강제 종료 토픽이 들어오면 수동 종료 경로도 지원합니다.
- 최종적으로 드론과 모바일 로봇은 순찰 상태로 복귀합니다.

## 빌드와 실행

이 프로젝트는 ROS 2 메타파일을 포함하지만, 실제 런타임은 Isaac Sim 환경 의존성이 큽니다.

예시:

```bash
source /opt/ros/humble/setup.bash
cd <workspace-root>
colcon build --symlink-install
source install/setup.bash
ros2 run warehouse_emergency_supervisor warehouse_supervisor --help
```

실제 실행 시에는 Isaac Sim Python, USD 자산 경로, 외부 환경 파일 배치가 함께 맞아야 합니다.

## 참고

- 데모 영상은 `docs/warehouse-emergency-supervisor-demo-video.mp4`로 관리합니다.
- 발표자료와 보고서는 로컬 `docs/`에 `warehouse-emergency-supervisor-*` 형식으로 정리했습니다.
- 코드와 런타임 자산은 `src/warehouse_emergency_supervisor/` 아래만 보면 됩니다.
