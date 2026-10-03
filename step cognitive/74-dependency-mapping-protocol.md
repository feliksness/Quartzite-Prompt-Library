# Dependency Mapping Protocol

*Maps what blocks what so tasks aren't attempted out of order.*

```
Map the dependencies in this plan:

1. List every task and, for each, exactly what it needs to be complete before it can start.
2. Check for hidden dependencies that aren't obvious from the task names alone.
3. Identify any circular dependency and resolve it before proceeding.
4. Order the plan so nothing starts before its true prerequisites are done.
```
