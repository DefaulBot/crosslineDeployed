-- inserts base types
INSERT INTO `auth_group` VALUES (2,'operator'),(1,'owner'),(3,'passenger');
-- assigns permission to group types
INSERT INTO `auth_group_permissions` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,1,5),(6,1,6),(7,1,7),(8,1,8),(9,1,9),(10,1,10),(11,1,11),(12,1,12),(13,1,13),(14,1,14),(15,1,15),(16,1,16),(17,1,17),(18,1,18),(19,1,19),(20,1,20),(21,1,21),(22,1,22),(23,1,23),(24,1,24),(27,2,14),(25,2,16),(26,2,24);

--adds admin user to owner group
INSERT INTO `auth_user_groups` VALUES (1,1,1);