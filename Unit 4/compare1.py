for nb in edges[city1]:
            neighbor = nb[0]
            new_distance = distances[city1] + nb[1]
            node1 = nodes[neighbor]
            node2 = nodes[target]
            estimate = calcd(node1, node2)
            if (new_distance < distances[neighbor] ):
                distances[neighbor] = new_distance
                newpath = list(v1[2])
                newpath.append(neighbor)
                heapq.heappush(q1, (distances[neighbor]+estimate, neighbor, newpath))
                visited1.add(neighbor)
                map1[neighbor] = newpath

                if neighbor in visited2:
                    list1 = map1[neighbor]
                    if len(list1) > 0:
                        list1.pop()
                        list1.reverse()
                    print("biA* meet from front distance=", distances[neighbor]+distances_target[neighbor])
                    draw_final_route(map2[neighbor] + list1, r, c)
                    return
            draw_search_route(city1, neighbor, r, c)