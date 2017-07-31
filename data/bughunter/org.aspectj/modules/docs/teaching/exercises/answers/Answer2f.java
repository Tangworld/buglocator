/* *******************************************************************
 * Copyright (c) 2002 Palo Alto Research Center, Incorporated (PARC).
 * All rights reserved.
 * This program and the accompanying materials are made available
 * under the terms of the Eclipse Public License v1.0
 * which accompanies this distribution and is available at
 * http://www.eclipse.org/legal/epl-v10.html
 *
 * Contributors:
 *     PARC     initial implementation
 * ******************************************************************/

package answers;

import figures.*;

import java.awt.Rectangle;

aspect Answer2f {
    void around(FigureElement fe, int dx, int dy):
            target(fe) && call(void move(int, int)) && args(dx, dy) {

        Rectangle preBounds = new Rectangle(fe.getBounds());
        proceed(fe, dx, dy);

        preBounds.translate(dx, dy);

        if (!preBounds.equals(fe.getBounds())) {
            throw new IllegalStateException("bounds don't match move");
        }
    }
}
